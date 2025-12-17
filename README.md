# 🎤 Voice Note Summarizer

A Streamlit-based web application that allows users to record or upload voice notes, automatically transcribe speech to text, correct grammar, and generate concise summaries using AI-powered NLP models.

---

##  Features

-  Record voice notes (auto-stops after 7 seconds)
-  Upload audio files (`.wav`, `.mp3`, `.ogg`, `.m4a`)
-  Speech-to-text transcription
-  Grammar correction for clean text
-  Automatic text summarization
-  Saves transcript, corrected text, and summary
-  Simple and interactive web interface

---

## Technology Stack

- **Frontend:** Streamlit  
- **Speech Recognition:** Transformer-based ASR  
- **NLP Models:** Transformers  
- **Audio Processing:** PyDub, SoundFile, FFmpeg  
- **Backend:** Python  
- **Deployment:** Render  

---

## 📂 Project Structure

    voice_note_summarizer/
        │
        ├── app/
        │ ├── app.py
        │ ├── transcriber.py
        │ ├── grammar.py
        │ ├── summarizer.py
        │
        ├── uploads/
        ├── recordings/
        ├── summaries/
        ├── output/
        │
        ├── requirements.txt
        ├── runtime.txt
        ├── render.yaml
        ├── .gitignore
        ├── LICENSE
        └── README.md

---

## Deployment

https://voice-note-summarizer.onrender.com
This application is deployed using Render.

---

## Notes

Runs on CPU (free-tier friendly)
First run may take time to load models
Large model files are excluded from GitHub

---

## Future Scope

Support for longer recordings
Multi-language transcription
Faster inference with optimized models

---

## License

This project is licensed under the MIT License.

## Author

HARSHITHA M V | AIML Engineer
