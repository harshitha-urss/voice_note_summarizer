import speech_recognition as sr
from transformers import pipeline
import os

AUDIO_DIR = "sample_voice_notes"

recognizer = sr.Recognizer()
corrector = pipeline("text2text-generation", model="./grammar_model")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

for file in os.listdir(AUDIO_DIR):
    if file.endswith('.wav') or file.endswith('.mp3'):
        path = os.path.join(AUDIO_DIR, file)
        try:
            with sr.AudioFile(path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)

            corrected = corrector("fix: " + text, max_length=128)[0]["generated_text"]
            summary = summarizer(corrected, max_length=40, min_length=10)[0]["summary_text"]

            print(f"\n📌 {file}")
            print("Raw:", text)
            print("Corrected:", corrected)
            print("Summary:", summary)

        except Exception as e:
            print(f"{file}: ERROR -> {e}")
