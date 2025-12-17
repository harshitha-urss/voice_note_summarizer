from pydub import AudioSegment
import os

# Convert all mp3 files in your folder to wav
for file in os.listdir():
    if file.endswith('.mp3'):
        sound = AudioSegment.from_mp3(file)
        wav_file = file.replace('.mp3', '.wav')
        sound.export(wav_file, format='wav')
        print(f'Converted {file} to {wav_file}')

# Convert all flac files to wav (for LibriSpeech)
for file in os.listdir():
    if file.endswith('.flac'):
        sound = AudioSegment.from_file(file, format='flac')
        wav_file = file.replace('.flac', '.wav')
        sound.export(wav_file, format='wav')
        print(f'Converted {file} to {wav_file}')
