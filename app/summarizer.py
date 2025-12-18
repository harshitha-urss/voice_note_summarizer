# summarizer.py
import os
import math
import streamlit as st
from transformers import pipeline

# ======================================================
# MODEL CONFIG
# ======================================================

SUMMARIZER_MODEL = os.getenv(
    "SUMMARIZER_MODEL",
    "sshleifer/distilbart-cnn-12-6"
)

# ======================================================
# LOAD MODEL (CACHED – LOADS ONLY ONCE)
# ======================================================

@st.cache_resource(show_spinner="Loading summarization model...")
def load_summarizer():
    """
    Loads the Hugging Face summarization pipeline once.
    Cached across Streamlit reruns to prevent memory crashes.
    """
    return pipeline(
        "summarization",
        model=SUMMARIZER_MODEL,
        device=-1  # CPU only (Render-safe)
    )

# ======================================================
# UTILS
# ======================================================

def _word_count(text: str) -> int:
    return len(text.strip().split())

# ======================================================
# MAIN SUMMARIZATION FUNCTION
# ======================================================

def summarize_text(text: str) -> str:
    """
    Summarizes input text safely with fallback logic.
    """

    text = (text or "").strip()
    if not text:
        return ""

    wc = _word_count(text)

    # If text is already short, return as-is
    if wc <= 12:
        return text

    # Dynamic length control
    max_len = max(20, min(80, math.ceil(wc * 0.45)))
    min_len = max(10, max_len - 10)

    try:
        summarizer = load_summarizer()

        output = summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False,
            truncation=True
        )

        if isinstance(output, list) and "summary_text" in output[0]:
            summary = output[0]["summary_text"].strip()

            # Safety check: summary should be shorter
            if _word_count(summary) >= wc:
                return text

            return summary

        return str(output)

    except Exception as e:
        # Graceful fallback (no crash)
        print("Summarizer error:", e)

        # Fallback: first 2 sentences
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        return ". ".join(sentences[:2]) + "."
