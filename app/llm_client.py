"""
Thin wrapper around the Gemini API (free tier) so the rest of the app
never touches the SDK directly. Swap this one file if you later move
to a paid provider — nothing else in the app needs to change.
"""
import json
import time
from google import genai
from google.genai import types
from google.genai.errors import ServerError
from app.config import settings

_client = genai.Client(api_key=settings.GEMINI_API_KEY)


def _generate_with_retry(model, contents, config, max_retries: int = 4):
    """
    Free-tier Gemini models occasionally return 503 'high demand' errors.
    Retry a few times with increasing wait before giving up.
    """
    delay = 2
    last_error = None
    for attempt in range(max_retries):
        try:
            return _client.models.generate_content(model=model, contents=contents, config=config)
        except ServerError as e:
            last_error = e
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
    raise last_error


def ask_llm_json(system_prompt: str, user_prompt: str, max_tokens: int = 2000) -> dict:
    """
    Calls Gemini and expects a JSON object back. Used for every
    'structured reasoning' step (parsing, analysis, scoring).
    """
    response = _generate_with_retry(
        model=settings.GEMINI_MODEL,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt + "\n\nRespond with ONLY valid JSON. No prose, no markdown fences.",
            response_mime_type="application/json",
            max_output_tokens=max_tokens,
        ),
    )
    text = (response.text or "").strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini did not return valid JSON: {e}\nRaw output: {text[:500]}")


def ask_llm_with_tools(system_prompt: str, user_prompt: str, tool_functions: list, max_tokens: int = 2000) -> str:
    """
    Runs a real agent loop: Gemini decides whether it needs to call one
    of the given Python functions (e.g. searching for learning resources
    for a missing skill), the SDK executes it automatically, feeds the
    result back, and returns Gemini's final text answer.

    tool_functions: plain Python functions with type hints + docstrings —
    the SDK reads those to build the tool schema automatically.
    """
    response = _generate_with_retry(
        model=settings.GEMINI_MODEL,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=tool_functions,
            max_output_tokens=max_tokens,
        ),
    )
    return response.text or "The agent did not return a final answer."