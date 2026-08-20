"""LLM-based speech coaching feedback using Anthropic API."""
import json
import os
from datetime import datetime, timezone

from anthropic import Anthropic


def get_coaching_feedback(transcription, mode, topic_text, framework_slug, metrics_dict):
    """
    Generate LLM-based coaching feedback for a recording.

    Args:
        transcription (str): User's speech transcript
        mode (dict): Mode object with 'name', 'slug'
        topic_text (str): The topic/prompt they were speaking about
        framework_slug (str): Framework used (STAR, PREP, or None)
        metrics_dict (dict): Deterministic metrics {
            'pace_wpm': float,
            'hedge_count': int,
            'filler_words': int,
            'concreteness_ratio': float,
            'time_to_point_seconds': float,
            'long_pause_count': int
        }

    Returns:
        dict or None: {
            'focus_area': str (one of 7 areas),
            'focus_reason': str,
            'landing_strength': str (weak/medium/strong),
            'strongest_moment': str (excerpt),
            'coach_notes': dict (structured feedback),
            'framework_adherence': dict (if framework provided)
        }
        Returns None if LLM call fails (graceful degradation).
    """
    if not transcription or not transcription.strip():
        return None

    try:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return None

        client = Anthropic(api_key=api_key)

        prompt = _build_coaching_prompt(
            transcription=transcription,
            mode_name=mode.get("name") if isinstance(mode, dict) else mode.name,
            topic_text=topic_text,
            framework_slug=framework_slug,
            metrics_dict=metrics_dict
        )

        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1500,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response_text = ""
        for block in response.content:
            if hasattr(block, 'text'):
                response_text = block.text
                break

        coaching_data = _parse_coaching_response(response_text)

        if coaching_data is None:
            return None

        return coaching_data

    except Exception as e:
        print(f"LLM coaching failed (graceful fallback): {e}")
        return None


def _build_coaching_prompt(transcription, mode_name, topic_text, framework_slug, metrics_dict):
    """Build the prompt for Claude to analyze speech."""

    framework_context = ""
    if framework_slug and framework_slug.upper() == "STAR":
        framework_context = """
Framework: STAR (Situation, Task, Action, Result)
- Evaluate how well they set up the situation
- Did they clearly explain the task/challenge?
- Were their actions specific and impactful?
- Did they wrap up with clear results/outcomes?
"""
    elif framework_slug and framework_slug.upper() == "PREP":
        framework_context = """
Framework: PREP (Point, Reason, Example, Point)
- Did they start with a clear point?
- Did they provide reasoning/context?
- Did they give concrete examples?
- Did they restate/reinforce the point?
"""

    metrics_summary = f"""
Speech Metrics:
- Pace: {metrics_dict.get('pace_wpm', 0):.1f} words/min (ideal: 120-150)
- Hedge phrases: {metrics_dict.get('hedge_count', 0)} (e.g., "kind of", "maybe")
- Filler words: {metrics_dict.get('filler_words', 0)} (e.g., "um", "uh")
- Concreteness: {metrics_dict.get('concreteness_ratio', 0):.1%} (higher = more specific)
- Time to main point: {metrics_dict.get('time_to_point_seconds', 0):.1f}s (lower = faster)
- Long pauses (>1.5s): {metrics_dict.get('long_pause_count', 0)}
"""

    prompt = f"""You are a professional speaking coach analyzing a practice recording.

Mode: {mode_name}
Topic: {topic_text}
{framework_context}

TRANSCRIPT:
---
{transcription}
---

{metrics_summary}

Please analyze this speech and provide constructive coaching feedback in valid JSON format.

CRITICAL: Your response MUST be ONLY valid JSON - no markdown, no code blocks, no explanations. Just pure JSON.

The 7 focus areas for coaching are: structure, concision, conviction, concreteness, pacing, storytelling, technical-clarity

Respond with this JSON structure:
{{
  "focus_area": "<ONE of: structure, concision, conviction, concreteness, pacing, storytelling, technical-clarity>",
  "focus_reason": "<Why this area needs work (1 sentence)>",
  "landing_strength": "<weak|medium|strong>",
  "strongest_moment": "<Direct quote from transcript of their best moment (2-10 words)>",
  "coach_notes": {{
    "opening": "<How strong was their opening? (1-2 sentences)>",
    "clarity": "<Was the main idea clear? (1-2 sentences)>",
    "evidence": "<Did they use examples/data? (1-2 sentences)>",
    "conclusion": "<How well did they wrap up? (1-2 sentences)>"
  }},
  "framework_adherence": {{
    "step_1": "<assessment (weak|medium|strong)>",
    "step_2": "<assessment (weak|medium|strong)>",
    "step_3": "<assessment (weak|medium|strong)>",
    "step_4": "<assessment (weak|medium|strong)>"
  }}
}}

Guidelines:
- Be specific and constructive
- Reference actual parts of the speech
- If framework is not provided, return empty framework_adherence
- Strongest_moment must be an actual quote from the transcript (verbatim)
- Focus on ONE primary area for improvement
"""

    return prompt


def _parse_coaching_response(response_text):
    """
    Parse Claude's JSON response defensively.

    Returns dict if valid and complete, None otherwise.
    """
    if not response_text or not response_text.strip():
        return None

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        print(f"Failed to parse JSON response: {response_text[:200]}")
        return None

    if not isinstance(data, dict):
        print(f"Response is not a dict: {type(data)}")
        return None

    VALID_FOCUS_AREAS = {
        "structure", "concision", "conviction", "concreteness",
        "pacing", "storytelling", "technical-clarity"
    }
    VALID_STRENGTHS = {"weak", "medium", "strong"}

    required_keys = {"focus_area", "focus_reason", "landing_strength", "strongest_moment", "coach_notes"}
    if not required_keys.issubset(data.keys()):
        print(f"Missing required keys. Got: {data.keys()}")
        return None

    focus_area = data.get("focus_area", "").lower().strip()
    if focus_area not in VALID_FOCUS_AREAS:
        print(f"Invalid focus_area: {focus_area}")
        return None

    landing_strength = data.get("landing_strength", "").lower().strip()
    if landing_strength not in VALID_STRENGTHS:
        print(f"Invalid landing_strength: {landing_strength}")
        return None

    coach_notes = data.get("coach_notes")
    if not isinstance(coach_notes, dict):
        print(f"coach_notes is not a dict")
        return None

    return {
        "focus_area": focus_area,
        "focus_reason": str(data.get("focus_reason", "")).strip(),
        "landing_strength": landing_strength,
        "strongest_moment": str(data.get("strongest_moment", "")).strip(),
        "coach_notes": coach_notes,
        "framework_adherence": data.get("framework_adherence", {})
    }
