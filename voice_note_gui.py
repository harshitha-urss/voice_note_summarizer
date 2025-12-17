    import os
import queue
import threading
import time
import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from transformers import pipeline

# -----------------------------
# CONFIG
# -----------------------------
AUDIO_DIR = "recordings"
OUTPUT_DIR = "output"
GRAMMAR_MODEL_PATH = "./grammar_model"   # your local grammar model folder
SUMMARIZER_MODEL = "facebook/bart-large-cnn"
SAMPLE_RATE = 16000
CHANNELS = 1

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# GLOBALS (pipelines loaded once)
# -----------------------------
print("Loading models (this may take a few seconds)...")
try:
    corrector = pipeline("text2text-generation", model=GRAMMAR_MODEL_PATH)
except Exception as e:
    corrector = None
    print("Warning: grammar model failed to load:", e)

try:
    summarizer = pipeline("summarization", model=SUMMARIZER_MODEL)
except Exception as e:
    summarizer = None
    print("Warning: summarizer failed to load:", e)

recognizer = sr.Recognizer()

# -----------------------------
# AUDIO RECORDING HELPERS
# -----------------------------
_audio_thread = None
_recording = False
_filename = None

def _record_to_file(filename, q, event):
    """Stream from microphone and save to file using soundfile."""
    with sf.SoundFile(filename, mode='x', samplerate=SAMPLE_RATE,
                      channels=CHANNELS, subtype='PCM_16') as file:
        def callback(indata, frames, time_info, status):
            if status:
                print("Recording status:", status)
            file.write(indata.copy())
            # stop if event set
            if event.is_set():
                raise sd.CallbackStop()

        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback):
            while not event.is_set():
                sd.sleep(100)  # small sleep to keep thread alive

def start_recording(ui_update_callback=None):
    global _audio_thread, _recording, _filename
    if _recording:
        return None
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(AUDIO_DIR, f"recording_{timestamp}.wav")
    stop_event = threading.Event()
    t = threading.Thread(target=_record_to_file, args=(filename, None, stop_event), daemon=True)
    t._stop_event = stop_event
    t.start()
    _audio_thread = t
    _recording = True
    _filename = filename
    if ui_update_callback:
        ui_update_callback("Recording started...")
    return filename

def stop_recording(ui_update_callback=None):
    global _audio_thread, _recording, _filename
    if not _recording or _audio_thread is None:
        return None
    _audio_thread._stop_event.set()
    _audio_thread.join()
    fname = _filename
    _audio_thread = None
    _recording = False
    _filename = None
    if ui_update_callback:
        ui_update_callback(f"Recording saved: {fname}")
    return fname

# -----------------------------
# TRANSCRIBE / PROCESS
# -----------------------------
def transcribe_file(filepath):
    """Return raw transcript (using Google Web Speech via speech_recognition)."""
    with sr.AudioFile(filepath) as source:
        audio_data = recognizer.record(source)
    # Using Google's free API (requires internet)
    text = recognizer.recognize_google(audio_data)
    return text

def correct_text(text):
    if corrector is None:
        raise RuntimeError("Grammar corrector model not loaded.")
    # Use prompt required by your local T5-style grammar model:
    prompt = "fix: " + text
    out = corrector(prompt, max_length=512)
    return out[0]["generated_text"]

def summarize_text(text):
    if summarizer is None:
        raise RuntimeError("Summarizer model not loaded.")
    out = summarizer(text, max_length=60, min_length=10, do_sample=False)
    return out[0]["summary_text"]

def process_audio_file(filepath):
    """Full pipeline for one file: transcribe -> correct -> summarize"""
    raw = transcribe_file(filepath)
    corrected = correct_text(raw)
    summary = summarize_text(corrected)
    return raw, corrected, summary

# -----------------------------
# CSV SAVE
# -----------------------------
def save_result_csv(original, corrected, summary, audio_path):
    csv_path = os.path.join(OUTPUT_DIR, "voice_note_results.csv")
    header_needed = not os.path.exists(csv_path)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if header_needed:
            writer.writerow(["timestamp", "audio_file", "original", "corrected", "summary"])
        writer.writerow([datetime.now().isoformat(), audio_path, original, corrected, summary])
    return csv_path

# -----------------------------
# TKINTER UI
# -----------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Voice Note Summarizer")
        self.geometry("820x560")
        self.resizable(False, False)

        frm = ttk.Frame(self, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)

        # Buttons
        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill=tk.X, pady=(0,8))

        self.record_btn = ttk.Button(btn_frame, text="Record", command=self.on_record)
        self.record_btn.pack(side=tk.LEFT, padx=4)

        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.on_stop, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=4)

        self.process_btn = ttk.Button(btn_frame, text="Process (Transcribe → Correct → Summarize)", command=self.on_process, state=tk.DISABLED)
        self.process_btn.pack(side=tk.LEFT, padx=8)

        self.open_csv_btn = ttk.Button(btn_frame, text="Open CSV folder", command=self.open_output_folder)
        self.open_csv_btn.pack(side=tk.RIGHT)

        # Status
        self.status = tk.StringVar(value="Ready")
        ttk.Label(frm, textvariable=self.status).pack(fill=tk.X)

        # Results area
        result_frame = ttk.Frame(frm)
        result_frame.pack(fill=tk.BOTH, expand=True)

        # Raw transcript
        ttk.Label(result_frame, text="Raw Transcript:").grid(row=0, column=0, sticky="w")
        self.raw_text = tk.Text(result_frame, height=8, width=95)
        self.raw_text.grid(row=1, column=0, padx=4, pady=4)

        # Corrected text
        ttk.Label(result_frame, text="Grammar-corrected:").grid(row=2, column=0, sticky="w")
        self.corrected_text = tk.Text(result_frame, height=6, width=95)
        self.corrected_text.grid(row=3, column=0, padx=4, pady=4)

        # Summary
        ttk.Label(result_frame, text="Summary:").grid(row=4, column=0, sticky="w")
        self.summary_text = tk.Text(result_frame, height=4, width=95)
        self.summary_text.grid(row=5, column=0, padx=4, pady=4)

        # Keep last recorded file path
        self.last_audio = None

    # UI actions
    def on_record(self):
        try:
            # disable record, enable stop
            self.record_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.process_btn.config(state=tk.DISABLED)
            self.status.set("Recording... Click Stop when finished.")
            # start recording thread
            threading.Thread(target=self._record_thread, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording: {e}")
            self.record_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)

    def _record_thread(self):
        fname = start_recording(self._ui_update)
        # wait here while recording; start_recording returns immediately — stop via button
        # Nothing else to do here.
        return

    def on_stop(self):
        try:
            self.stop_btn.config(state=tk.DISABLED)
            self.record_btn.config(state=tk.NORMAL)
            saved = stop_recording(self._ui_update)
            if saved:
                self.last_audio = saved
                self.process_btn.config(state=tk.NORMAL)
                self.status.set(f"Saved: {saved} — click Process to transcribe & summarize.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop recording: {e}")

    def on_process(self):
        if not self.last_audio or not os.path.exists(self.last_audio):
            messagebox.showwarning("No audio", "No recorded audio found. Please record first.")
            return
        # disable buttons during processing
        self.process_btn.config(state=tk.DISABLED)
        self.record_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
        self.status.set("Processing: transcribing...")
        threading.Thread(target=self._process_thread, daemon=True).start()

    def _process_thread(self):
        try:
            raw, corrected, summary = process_audio_file(self.last_audio)
            # update UI (must be done in main thread)
            self.after(0, lambda: self.raw_text.delete("1.0", tk.END))
            self.after(0, lambda: self.raw_text.insert(tk.END, raw))
            self.after(0, lambda: self.corrected_text.delete("1.0", tk.END))
            self.after(0, lambda: self.corrected_text.insert(tk.END, corrected))
            self.after(0, lambda: self.summary_text.delete("1.0", tk.END))
            self.after(0, lambda: self.summary_text.insert(tk.END, summary))
            csv_path = save_result_csv(raw, corrected, summary, self.last_audio)
            self.after(0, lambda: self.status.set(f"Done. Saved results to {csv_path}"))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Processing Error", str(e)))
            self.after(0, lambda: self.status.set("Error during processing."))
        finally:
            self.after(0, lambda: self.process_btn.config(state=tk.NORMAL))
            self.after(0, lambda: self.record_btn.config(state=tk.NORMAL))
            self.after(0, lambda: self.stop_btn.config(state=tk.DISABLED))

    def _ui_update(self, text):
        self.after(0, lambda: self.status.set(text))

    def open_output_folder(self):
        path = os.path.abspath(OUTPUT_DIR)
        try:
            if os.name == "nt":
                os.startfile(path)
            else:
                import subprocess
                subprocess.run(["xdg-open", path])
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open folder: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
