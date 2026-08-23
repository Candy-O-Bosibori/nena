import React, { useEffect, useRef, useState } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import api from "../../api/api";
import CircularTimer from "../../Components/CircularTimer/CircularTimer";
import Button from "../../Components/ui/Button";

export const Practice = () => {
  const { modeSlug } = useParams();
  const navigate = useNavigate();
  const location = useLocation();

  // Get topic/mode/framework from router state
  const { topic: routerTopic, mode: routerMode, selectedFramework } = location.state || {};

  const audioRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const recordedChunksRef = useRef([]);
  const timerRef = useRef(null);
  const streamRef = useRef(null);

  const [stream, setStream] = useState(null);
  const [recording, setRecording] = useState(false);
  const [paused, setPaused] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [recordingId, setRecordingId] = useState(null);
  const [micLabel, setMicLabel] = useState("");
  // Mirrors recordedChunksRef in React state: mutating a ref's .current
  // doesn't trigger a re-render, so the Submit/Discard/playback UI needs its
  // own state to actually show up once a recording has stopped.
  const [previewUrl, setPreviewUrl] = useState(null);

  // Guard: redirect if no router state (direct URL navigation)
  useEffect(() => {
    if (!location.state?.topic || !location.state?.mode) {
      toast.error("No topic selected — pick one from Overview first", {
        autoClose: 2500,
        position: "top-center",
      });
      navigate("/overview", { replace: true });
    }
  }, []);

  // Get mic permission (bug fix #2: use streamRef for cleanup)
  useEffect(() => {
    let cancelled = false;

    const startMicrophone = async () => {
      try {
        const mediaStream = await navigator.mediaDevices.getUserMedia({
          audio: {
            echoCancellation: true,
            noiseSuppression: true,
            autoGainControl: true,
          },
          video: false,
        });
        if (cancelled) {
          mediaStream.getTracks().forEach((t) => t.stop());
          return;
        }

        // Show which input is in use, so a wrong device is obvious before recording.
        const track = mediaStream.getAudioTracks()[0];
        setMicLabel(track?.label || "unknown device");

        streamRef.current = mediaStream;
        setStream(mediaStream);
      } catch (err) {
        toast.error("❌ Microphone access denied!");
      }
    };

    startMicrophone();

    return () => {
      cancelled = true;
      streamRef.current?.getTracks().forEach((track) => track.stop());
    };
  }, []);

  // Revoke the blob URL on unmount so navigating away doesn't leak it.
  useEffect(() => {
    return () => {
      if (previewUrl) URL.revokeObjectURL(previewUrl);
    };
  }, [previewUrl]);

  // Start recording
  const startRecording = () => {
    recordedChunksRef.current = [];
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      setPreviewUrl(null);
    }

    if (!stream) {
      toast.error("Microphone not available!");
      return;
    }

    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorderRef.current = mediaRecorder;

    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) {
        recordedChunksRef.current.push(e.data);
      }
    };

    // onstop fires once all buffered data has been flushed to
    // recordedChunksRef, so this is the reliable point to build a preview --
    // building it in the click handler that calls stop() would race the
    // final dataavailable event.
    mediaRecorder.onstop = () => {
      if (recordedChunksRef.current.length === 0) return;
      const blob = new Blob(recordedChunksRef.current, { type: "audio/webm" });
      setPreviewUrl(URL.createObjectURL(blob));
    };

    mediaRecorder.start();
    setRecording(true);
    setPaused(false);

    timerRef.current?.start();
  };

  // Pause recording
  const pauseRecording = () => {
    mediaRecorderRef.current?.pause();
    timerRef.current?.pause();
    setPaused(true);
  };

  // Resume recording
  const resumeRecording = () => {
    mediaRecorderRef.current?.resume();
    timerRef.current?.resume();
    setPaused(false);
  };

  // Stop recording. Called both by the Stop button and by the timer's
  // onComplete, so it must be safe to invoke more than once.
  const stopRecording = () => {
    const recorder = mediaRecorderRef.current;
    if (recorder && recorder.state !== "inactive") {
      recorder.stop();
    }
    timerRef.current?.pause();
    setRecording(false);
    setPaused(false);
  };

  // Delete recording / start over
  const deleteRecording = () => {
    recordedChunksRef.current = [];
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(null);
    setRecording(false);
    setPaused(false);
    timerRef.current?.reset();
    toast.success("Recording deleted!", {
      position: "top-center",
      autoClose: 2000,
    });
  };

  // Submit recording
  const submitRecording = async () => {
    if (recordedChunksRef.current.length === 0) {
      toast.error("No recording available.");
      return;
    }

    setSubmitting(true);

    const blob = new Blob(recordedChunksRef.current, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("mode_id", routerMode?.id || 1);
    if (routerTopic?.id) formData.append("topic_id", routerTopic.id);
    if (selectedFramework) formData.append("framework_slug", selectedFramework);
    formData.append("video", blob, `recording-${Date.now()}.webm`);

    try {
      const response = await api.post("/recordings", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setRecordingId(response.data.id);
      if (response.data.transcription_ok === false) {
        toast.warn(
          response.data.transcription_error ||
            "No speech detected — check your microphone.",
          { autoClose: 6000, position: "top-center" }
        );
      }
      setShowModal(true);
      recordedChunksRef.current = [];
      if (previewUrl) URL.revokeObjectURL(previewUrl);
      setPreviewUrl(null);
    } catch (error) {
      toast.error("Failed to submit recording");
      console.error("Submit error:", error);
    } finally {
      setSubmitting(false);
    }
  };

  if (!routerMode || !routerTopic) {
    return null;
  }

  return (
    <div className="min-h-screen bg-cream">
      <ToastContainer />

      <div className="mx-auto flex min-h-screen w-full max-w-2xl flex-col px-5 py-8">
        {/* Back link */}
        <button
          onClick={() => navigate("/overview")}
          className="self-start rounded-xl px-2 py-1 text-sm font-semibold text-ink-soft transition-colors hover:text-primary focus-ring"
        >
          ← Back
        </button>

        {/* Main content: centered column */}
        <div className="flex flex-1 flex-col items-center justify-center gap-9 py-6">
          {/* Topic reminder */}
          <div className="w-full text-center">
            <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-ink-muted">
              Your topic
            </p>
            <p
              className={`mx-auto mt-3 max-w-xl font-semibold text-ink ${
                routerMode.slug === "read-aloud"
                  ? "text-lg leading-relaxed md:text-xl"
                  : "text-xl md:text-2xl"
              }`}
            >
              {routerTopic.text || routerTopic.meta?.word}
            </p>

            <div className="mt-4 flex flex-wrap items-center justify-center gap-2">
              {selectedFramework && (
                <span className="rounded-full bg-primary-soft px-3 py-1 text-[11px] font-bold uppercase tracking-[0.12em] text-primary-700">
                  {selectedFramework}
                </span>
              )}
              {micLabel && (
                <span className="max-w-[260px] truncate rounded-full border border-line bg-surface px-3 py-1 text-[11px] font-medium text-ink-muted">
                  🎙 {micLabel}
                </span>
              )}
            </div>
          </div>

          {/* Circular Timer */}
          <CircularTimer
            ref={timerRef}
            durationSeconds={routerMode?.default_timer_seconds || 60}
            mode={routerMode?.slug === "read-aloud" ? "countup" : "countdown"}
            onComplete={stopRecording}
            accentColor={routerMode?.accent_color || "#DC9750"}
          />

          {/* Transport Controls */}
          <div className="flex items-center justify-center gap-4">
            {!recording ? (
              <button
                onClick={startRecording}
                aria-label="Start recording"
                className="flex h-20 w-20 items-center justify-center rounded-full bg-primary text-on-primary shadow-lg shadow-primary/25 transition-all duration-200 hover:bg-primary-hover active:scale-95 focus-ring"
              >
                <span className="block h-6 w-6 rounded-full bg-white" />
              </button>
            ) : (
              <>
                <button
                  onClick={paused ? resumeRecording : pauseRecording}
                  aria-label={paused ? "Resume recording" : "Pause recording"}
                  className="flex h-14 w-14 items-center justify-center rounded-full border border-line bg-surface text-ink shadow-sm transition-all duration-200 hover:border-ink-muted active:scale-95 focus-ring"
                >
                  {paused ? (
                    <span className="ml-0.5 block h-0 w-0 border-y-[9px] border-l-[14px] border-y-transparent border-l-ink" />
                  ) : (
                    <span className="flex gap-1">
                      <span className="block h-4 w-1.5 rounded-sm bg-ink" />
                      <span className="block h-4 w-1.5 rounded-sm bg-ink" />
                    </span>
                  )}
                </button>
                <button
                  onClick={stopRecording}
                  aria-label="Stop recording"
                  className="flex h-20 w-20 items-center justify-center rounded-full bg-danger text-white shadow-lg shadow-danger/25 transition-all duration-200 hover:brightness-95 active:scale-95 focus-ring"
                >
                  <span className="block h-5 w-5 rounded-[3px] bg-white" />
                </button>
              </>
            )}
          </div>

          {recording && (
            <p className="flex items-center gap-2 text-xs font-semibold text-danger">
              <span className="h-2 w-2 animate-pulse rounded-full bg-danger" />
              {paused ? "Paused" : "Recording"}
            </p>
          )}

          {/* Playback + Submit / Discard, once a recording exists and isn't
              still in progress -- driven by previewUrl (state), not the
              chunks ref, so this reliably re-renders when recording stops. */}
          {previewUrl && !recording && (
            <div className="flex w-full max-w-sm flex-col items-center gap-4">
              <audio ref={audioRef} src={previewUrl} controls className="w-full" />
              <div className="flex flex-wrap items-center justify-center gap-3">
                <Button onClick={submitRecording} disabled={submitting} size="lg">
                  {submitting ? "Submitting…" : "Submit for review"}
                </Button>
                <Button onClick={deleteRecording} variant="danger" size="lg">
                  Start over
                </Button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Success Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-ink/40 p-4 backdrop-blur-sm">
          <div className="w-full max-w-sm rounded-3xl bg-surface p-8 shadow-2xl animate-pop">
            <h2 className="font-display text-xl font-normal tracking-tight text-ink">
              Recording submitted
            </h2>
            <p className="mt-2 text-sm leading-relaxed text-ink-soft">
              We're analysing your delivery. Your feedback will be ready in a moment.
            </p>
            <div className="mt-6 flex flex-col gap-2">
              <Button onClick={() => navigate("/feedback")}>View feedback</Button>
              <Button onClick={() => navigate("/overview")} variant="ghost">
                Practice again
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
