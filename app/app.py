import streamlit as st
from audiorecorder import audiorecorder
from pathlib import Path

from transcriber import transcribe_audio
from grammar import correct_grammar
from summarizer import summarize_text

st.set_page_config(page_title="Voice Note Summarizer", layout="centered")

st.title("🎤 Voice Note Summarizer")
st.caption("Record → Transcribe → Correct Grammar → Summarize")

# Create folders
Path("uploads").mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)

st.markdown("---")

# ======================================================
# 1️⃣ AUDIO RECORDING — AUTO STOP AT 7 SECONDS
# ======================================================

st.subheader("Record Audio (Auto Stops After 7 Seconds)")

recorded_audio = audiorecorder("Start Recording", "Stop")

audio_path = None

if len(recorded_audio) > 0:
    st.success("Recording captured!")

    # 👉 Auto-trim to 7 seconds
    recorded_audio = recorded_audio[:7 * 1000]   # 7000 ms

    audio_path = "uploads/recorded_audio.wav"
    recorded_audio.export(audio_path, format="wav")

    st.audio(audio_path)

# ======================================================
# 2️⃣ UPLOAD AUDIO FILE
# ======================================================

st.subheader("Or Upload an Audio File")
uploaded = st.file_uploader("Upload .wav / .mp3 / .ogg / .m4a", type=["wav", "mp3", "ogg", "m4a"])

if uploaded:
    audio_path = f"uploads/{uploaded.name}"
    with open(audio_path, "wb") as f:
        f.write(uploaded.read())
    st.success("File uploaded")
    st.audio(audio_path)

st.markdown("---")

# ======================================================
# 3️⃣ PROCESS AUDIO
# ======================================================

if audio_path:
    st.info("Processing — this may take 10–30 seconds...")

    # TRANSCRIBE
    transcript = transcribe_audio(audio_path)

    # GRAMMAR FIX
    corrected = correct_grammar(transcript)

    # SUMMARY
    summary = summarize_text(corrected)

    # Display output
    st.markdown("### 📝 Transcript")
    st.write(transcript)

    st.markdown("### ✨ Grammar Corrected")
    st.write(corrected)

    st.markdown("### 📌 Summary")
    st.write(summary)

    # Save to file
    out_path = f"output/result_{Path(audio_path).stem}.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("Transcript:\n" + transcript)
        f.write("\n\nGrammar Corrected:\n" + corrected)
        f.write("\n\nSummary:\n" + summary)

    st.success(f"Saved results → {out_path}")
