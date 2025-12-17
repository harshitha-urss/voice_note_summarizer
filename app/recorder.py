# recorder.py
import os
from pathlib import Path
from datetime import datetime
import tempfile

# Save Streamlit uploaded file to disk and return path
def save_uploaded_audio(uploaded_file):
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    suffix = Path(uploaded_file.name).suffix or ".wav"
    # create unique filename
    out_path = uploads_dir / f"upload_{len(list(uploads_dir.iterdir()))+1}{suffix}"
    with open(out_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(out_path)

# Optional local recorder (works only when running locally with sounddevice)
def record_audio(duration=10, fs=16000):
    try:
        import sounddevice as sd
        from scipy.io.wavfile import write
    except Exception as e:
        raise RuntimeError("Local recording requires sounddevice and scipy. Install in your environment.") from e

    recordings_dir = Path("recordings")
    recordings_dir.mkdir(exist_ok=True)
    filename = recordings_dir / f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"

    # Simple recording (blocking)
    print("\n🎬 Recording will begin in:")
    for i in range(3, 0, -1):
        print(f"⏳ {i}...")
        import time
        time.sleep(1)
    print("🎤 Start speaking now!\n")

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    write(str(filename), fs, recording)
    print(f"🎧 Recording saved: {filename}")
    return str(filename)
