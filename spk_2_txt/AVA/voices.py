from google.cloud import speech
from google.cloud.speech import enums, types


def sample_recognition(remote_url):
    """
    :param remote_url: A URL to a GCloud Storage system
    :return: the transcription of the file at the remote url
    """
    remote_url = str(remote_url)
    url_parts = remote_url.split('/')
    uri = "gs://" + str(url_parts[-2]) + "/" + str(url_parts[-1])
    client = speech.SpeechClient()
    audio_channel_count = 2
    language_code = "en-US"
    # sample_rate_hertz = 16000
    #encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "audio_channel_count": audio_channel_count,
        "language_code": language_code,
        # "sample_rate_hertz" : sample_rate_hertz,
        # "encoding": encoding
    }

    audio = {"uri" : uri}

    response = client.recognize(config, audio)
    recognized_text = "Transcribed Text \n"
    for result in response.results:
        transcript = result.alternatives[0].transcript
    return transcript




