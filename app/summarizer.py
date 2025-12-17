# summarizer.py
import os
import math
from transformers import pipeline

SUMMARIZER_MODEL = os.environ.get("SUMMARIZER_MODEL", "sshleifer/distilbart-cnn-12-6")

_summarizer = None
def get_summarizer():
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline("summarization", model=SUMMARIZER_MODEL)
    return _summarizer

def _word_count(text: str) -> int:
    return len(text.strip().split())

def summarize_text(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    wc = _word_count(text)
    if wc <= 12:
        return text
    approx_max_tokens = max(10, min(50, math.ceil(wc * 0.5)))
    approx_min_tokens = max(5, approx_max_tokens - 5)
    try:
        summarizer = get_summarizer()
        out = summarizer(text, max_length=approx_max_tokens, min_length=approx_min_tokens, do_sample=False, truncation=True)
        if isinstance(out, list) and len(out) and "summary_text" in out[0]:
            summary = out[0]["summary_text"].strip()
            if len(summary.split()) > wc:
                return text
            return summary
        return str(out)
    except Exception as e:
        print("Summarizer error:", e)
        # fallback: first 2 sentences
        parts = text.split(".")
        return ". ".join([p.strip() for p in parts[:2] if p.strip()]) + "."
