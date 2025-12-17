import speech_recognition as sr
from transformers import pipeline

recognizer = sr.Recognizer()
corrector = pipeline("text2text-generation", model="./grammar_model")

print("Speak now...")

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

text = recognizer.recognize_google(audio)
print("Raw:", text)

corrected = corrector("fix: " + text)[0]["generated_text"]
print("Corrected:", corrected)
