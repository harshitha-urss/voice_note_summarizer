import speech_recognition as sr
import os

recognizer = sr.Recognizer()

for file in os.listdir():
    if file.endswith('.wav'):
        try:
            with sr.AudioFile(file) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                print(f"{file}: {text}")
        except Exception as e:
            print(f"{file}: ERROR -> {e}")
