# transcriber.py
from transformers import pipeline

# Load Whisper only once
print("⏳ Loading Whisper ASR model (openai/whisper-base)...")

asr = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-base",
    chunk_length_s=30   # safer for longer files
)

def transcribe_audio(path: str) -> str:
    """
    Transcribes an audio file and returns the text.
    Always returns a string (never crashes).
    """
    try:
        result = asr(path)
        if isinstance(result, dict) and "text" in result:
            return result["text"].strip()
        return str(result).strip()
    except Exception as e:
        print("ASR error:", e)
        return ""
