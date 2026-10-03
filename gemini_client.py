"""Shared Gemini configuration for the resume-analysis workflow."""

import os

import google.generativeai as genai
import streamlit as st


DEFAULT_MODEL = "gemini-3.6-flash"


def _get_setting(name: str) -> str | None:
    """Read a setting from the environment first, then Streamlit secrets."""
    value = os.getenv(name)
    if value:
        return value

    try:
        value = st.secrets.get(name)
    except (FileNotFoundError, KeyError):
        value = None
    return value or None


def configure_gemini() -> str:
    """Configure the legacy Gemini SDK and return the selected model name."""
    api_key = _get_setting("GEMINI_API_KEY")
    if not api_key or api_key == "your-google-gemini-api-key-here":
        raise ValueError(
            "GEMINI_API_KEY is not configured. Add it to Streamlit secrets or set it "
            "as an environment variable."
        )

    genai.configure(api_key=api_key)
    return _get_setting("GEMINI_MODEL") or DEFAULT_MODEL


def create_model(*, temperature: float):
    """Return a configured text model that is constrained to JSON responses."""
    model_name = configure_gemini()
    return genai.GenerativeModel(
        model_name,
        generation_config={
            "response_mime_type": "application/json",
            "temperature": temperature,
        },
    )
