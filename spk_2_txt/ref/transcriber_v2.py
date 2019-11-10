import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from tqdm import tqdm

with open("api-key.json") as f:
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

r = speech_v1.SpeechClient()

files = sorted(os.listdir('Audio/'))

encoding = enums.RecognitionConfig.AudioEncoding.FLAC
sample_rate_hertz = 44100
language_code = "en-US"
config = {'encoding': encoding, 'sample_rate_hertz': sample_rate_hertz, 'language_code': language_code}

all_text = []

for f in tqdm(files):
    name = "Audio/" + f
    # Loading in the audio
    with sr.AudioFile(name) as source:
        audio = r.record(source)
    # Transcription
    text = r.recognize(config, audio)
    all_text.append(text)


for name, text in zip(files,all_text):
    filename = name.split(".", 1)[0] + "_transcript.txt"
    with open( os.path.join("Text", filename), "w") as f:
        f.write(text)
