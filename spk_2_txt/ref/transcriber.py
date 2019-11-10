import os
import speech_recognition as sr
from tqdm import tqdm

with open("api-key.json") as f:
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

r = sr.Recognizer()

files = sorted(os.listdir('Audio/'))

all_text = []

for f in tqdm(files):
    name = "Audio/" + f
    # Loading in the audio
    with sr.AudioFile(name) as source:
        audio = r.record(source)
    # Transcription
    text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
    all_text.append(text)


for name, text in zip(files,all_text):
    filename = name.split(".", 1)[0] + "_transcript.txt"
    with open( os.path.join("Text", filename), "w") as f:
        f.write(text)
