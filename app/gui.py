from recorder import record_audio
from transcriber import transcribe_audio
from grammar import correct_grammar
from summarizer import summarize_text
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

OUTPUT_DIR = "output"
SUMMARIES_DIR = "summaries"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SUMMARIES_DIR, exist_ok=True)

def run_pipeline():
    print("\n============================")
    print("🎤 VOICE NOTE SUMMARIZER APP")
    print("============================")

    # 1. Record audio
    print("🎙️ Preparing to record... (Speak for 10 seconds)")
    audio_file = record_audio(duration=10)


    # 2. Transcribe
    text = transcribe_audio(audio_file)

    # 3. Grammar correction
    corrected = correct_grammar(text)

    # 4. Summarization
    summary = summarize_text(corrected)

    # Save outputs
    out_file = os.path.join(OUTPUT_DIR, "result.txt")
    sum_file = os.path.join(SUMMARIES_DIR, "summary.txt")

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("Original:\n" + text + "\n\nCorrected:\n" + corrected)

    with open(sum_file, "w", encoding="utf-8") as f:
        f.write(summary)

    print("\n✅ All outputs saved successfully!")
    print(f"📄 Full text: {out_file}")
    print(f"📄 Summary: {sum_file}")

if __name__ == "__main__":
    run_pipeline()
