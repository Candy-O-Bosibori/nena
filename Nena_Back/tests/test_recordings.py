"""Smoke tests for POST /recordings and GET /recordings.

External services (ffmpeg extraction/duration probing, AssemblyAI
transcription, the Anthropic coaching call) are mocked out -- these tests
check that the endpoint wires a valid Recording row together and enforces
auth/ownership, not that AssemblyAI or Anthropic are reachable.
"""
import io

import pytest

from models import Mode, Recording

FAKE_WEBM_BYTES = b"\x1a\x45\xdf\xa3fakewebmcontent"


@pytest.fixture
def mode(session):
    m = Mode(name="Wildcard", slug="random-topic", accent_color="#DC9750")
    session.add(m)
    session.commit()
    return m


@pytest.fixture(autouse=True)
def mock_external_services(mocker):
    """Applied to every test in this file -- POST /recordings always calls
    out to these, mocked or not, so there's no per-test opt-in needed."""
    mocker.patch("resources.recordings.extract_audio", return_value="/tmp/fake-audio.wav")
    mocker.patch("resources.recordings.transcribe_audio", return_value="this is a fake transcription")
    mocker.patch("resources.recordings.get_video_duration", return_value=42.0)
    mocker.patch("resources.feedback.get_coaching_feedback", return_value=None)


def _upload(client, headers, mode_id, filename="clip.webm"):
    data = {
        "mode_id": str(mode_id),
        "video": (io.BytesIO(FAKE_WEBM_BYTES), filename),
    }
    return client.post(
        "/recordings", data=data, headers=headers, content_type="multipart/form-data"
    )


def test_post_recording_creates_row_and_returns_201(client, auth_headers, mode):
    headers, user = auth_headers(email="uploader@example.com")

    resp = _upload(client, headers, mode.id)

    assert resp.status_code == 201
    body = resp.get_json()
    assert body["transcription_ok"] is True
    assert "recording_id" in body

    recording = Recording.query.filter_by(id=body["recording_id"]).first()
    assert recording is not None
    assert recording.user_id == user.id
    assert recording.mode_id == mode.id


def test_post_recording_without_auth_is_401(client, mode):
    resp = _upload(client, {}, mode.id)
    assert resp.status_code == 401


def test_post_recording_rejects_disallowed_extension(client, auth_headers, mode):
    headers, _ = auth_headers(email="badext@example.com")
    resp = _upload(client, headers, mode.id, filename="clip.exe")
    assert resp.status_code == 400


def test_get_recordings_only_returns_own(client, auth_headers, mode):
    headers_a, _ = auth_headers(email="usera@example.com")
    headers_b, user_b = auth_headers(email="userb@example.com")

    upload_resp = _upload(client, headers_a, mode.id)
    assert upload_resp.status_code == 201

    resp = client.get("/recordings", headers=headers_b)
    assert resp.status_code == 200
    assert resp.get_json() == []
