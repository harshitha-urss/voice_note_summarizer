import streamlit as st
from pathlib import Path

from transcriber import transcribe_audio
from grammar import correct_grammar
from summarizer import summarize_text

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Voice Note Summarizer",
    layout="centered"
)

st.title("🎤 Voice Note Summarizer")
st.caption("Upload Audio → Transcribe → Correct Grammar → Summarize")

# --------------------------------------------------
# Create folders
# --------------------------------------------------
Path("uploads").mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)

st.markdown("---")

# --------------------------------------------------
# 📤 UPLOAD AUDIO FILE (RENDER COMPATIBLE)
# --------------------------------------------------
st.subheader("Upload an Audio File")

uploaded = st.file_uploader(
    "Upload .wav / .mp3 / .ogg / .m4a",
    type=["wav", "mp3", "ogg", "m4a"]
)

audio_path = None

if uploaded:
    audio_path = f"uploads/{uploaded.name}"
    with open(audio_path, "wb") as f:
        f.write(uploaded.read())

    st.success("Audio uploaded successfully")
    st.audio(audio_path)

st.markdown("---")

# --------------------------------------------------
# 🚀 PROCESS AUDIO
# --------------------------------------------------
if audio_path:
    st.info("Processing audio… please wait ⏳")

    # 1️⃣ Transcription
    transcript = transcribe_audio(audio_path)

    # 2️⃣ Grammar correction
    corrected = correct_grammar(transcript)

    # 3️⃣ Summarization
    summary = summarize_text(corrected)

    # --------------------------------------------------
    # Display results
    # --------------------------------------------------
    st.subheader("📝 Transcript")
    st.write(transcript)

    st.subheader("✨ Grammar Corrected")
    st.write(corrected)

    st.subheader("📌 Summary")
    st.write(summary)

    # --------------------------------------------------
    # Save output
    # --------------------------------------------------
    out_path = f"output/result_{Path(audio_path).stem}.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("Transcript:\n")
        f.write(transcript)
        f.write("\n\nGrammar Corrected:\n")
        f.write(corrected)
        f.write("\n\nSummary:\n")
        f.write(summary)

    st.success(f"Results saved to `{out_path}`")
