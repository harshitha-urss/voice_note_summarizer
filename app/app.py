import os
import streamlit as st
from pathlib import Path

from transcriber import transcribe_audio
from grammar import correct_grammar
from summarizer import summarize_text

# ======================================================
# ENVIRONMENT DETECTION
# ======================================================

# Render always sets PORT
IS_RENDER = "PORT" in os.environ
IS_LOCAL = not IS_RENDER

# Import audiorecorder ONLY on localhost
if IS_LOCAL:
    try:
        from audiorecorder import audiorecorder
    except ImportError:
        audiorecorder = None

# ======================================================
# STREAMLIT CONFIG
# ======================================================

st.set_page_config(
    page_title="Voice Note Summarizer",
    layout="centered"
)

st.title("🎤 Voice Note Summarizer")
st.caption("Record / Upload → Transcribe → Correct Grammar → Summarize")

# Create folders
Path("uploads").mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)

audio_path = None

st.markdown("---")

# ======================================================
# 1️⃣ LIVE RECORDING (LOCALHOST ONLY)
# ======================================================

if IS_LOCAL and audiorecorder:
    st.subheader("🎙️ Record Audio (Localhost Only)")
    st.info("Live microphone recording is available only when running locally.")

    recorded_audio = audiorecorder("Start Recording", "Stop Recording")

    if recorded_audio is not None and len(recorded_audio) > 0:
        st.success("Recording captured!")

        # Limit to 7 seconds
        recorded_audio = recorded_audio[:7000]

        audio_path = "uploads/recorded_audio.wav"
        recorded_audio.export(audio_path, format="wav")

        st.audio(audio_path)

elif IS_RENDER:
    st.subheader("🎙️ Live Recording")
    st.warning("Live recording is disabled on cloud deployments (Render).")

# ======================================================
# 2️⃣ FILE UPLOAD (LOCAL + CLOUD)
# ======================================================

st.markdown("---")
st.subheader("📁 Upload an Audio File")

uploaded = st.file_uploader(
    "Upload .wav / .mp3 / .ogg / .m4a",
    type=["wav", "mp3", "ogg", "m4a"]
)

if uploaded:
    audio_path = f"uploads/{uploaded.name}"

    with open(audio_path, "wb") as f:
        f.write(uploaded.read())

    st.success("File uploaded successfully")
    st.audio(audio_path)

# ======================================================
# 3️⃣ PROCESS AUDIO
# ======================================================

if audio_path:
    st.markdown("---")
    st.info("Processing audio — please wait (10–30 seconds)...")

    # Transcription
    transcript = transcribe_audio(audio_path)

    # Grammar correction
    corrected = correct_grammar(transcript)

    # Summarization
    summary = summarize_text(corrected)

    # Display results
    st.markdown("### 📝 Transcript")
    st.write(transcript)

    st.markdown("### ✨ Grammar Corrected")
    st.write(corrected)

    st.markdown("### 📌 Summary")
    st.write(summary)

    # Save output
    out_path = f"output/result_{Path(audio_path).stem}.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("Transcript:\n" + transcript)
        f.write("\n\nGrammar Corrected:\n" + corrected)
        f.write("\n\nSummary:\n" + summary)

    st.success(f"Results saved → {out_path}")
