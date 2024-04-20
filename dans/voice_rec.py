from openai import OpenAI
from keys import opai_key
client = OpenAI(api_key=opai_key)


def rec_voice(filename):
    audio_file= open(filename, "rb")
    transcription = client.audio.transcriptions.create(
      model="whisper-1", 
      file=audio_file
    )
    print(transcription.text)

# rec_voice('./adata/1.wav')

def generate_voice_from_file(query):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=query,
    )

    response.stream_to_file("output.mp3")
