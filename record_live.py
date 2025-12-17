import sounddevice as sd
from scipy.io.wavfile import write

fs = 16000  # Sample rate
seconds = 5  # Record 5 seconds
print('Recording...')
recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
sd.wait()
write('live_note.wav', fs, recording)
print('Saved as live_note.wav')
