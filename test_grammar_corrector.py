import speech_recognition as sr
import os

AUDIO_DIR = "sample_voice_notes"

recognizer = sr.Recognizer()

for file in os.listdir(AUDIO_DIR):
    if file.endswith('.wav'):
        path = os.path.join(AUDIO_DIR, file)
        try:
            with sr.AudioFile(path) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio)
                print(f"{file}: {text}")
        except Exception as e:
            print(f"{file}: ERROR -> {e}")
