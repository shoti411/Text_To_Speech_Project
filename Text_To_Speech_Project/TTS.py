import os
from os.path import exists
import pandas as pd #  pip install numpy==1.19.3
from google.cloud import texttospeech # outdated or incomplete comparing to v1
from google.cloud import texttospeech_v1
from playsound import playsound
from time import sleep
import tkinter as tk
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "TTS_SVC_ACC.json"
# Instantiates a client
client = texttospeech_v1.TextToSpeechClient()
quote = """<speak>
    Here are <say-as interpret-as="characters">SSML</say-as> samples.
    I can pause <break time="3s"/>.
    I can play a sound
    <audio src="https://www.example.com/MY_MP3_FILE.mp3">didn't get your MP3 audio file</audio>.
    I can speak in cardinals. Your number is <say-as interpret-as="cardinal">10</say-as>.
    Or I can speak in ordinals. You are <say-as interpret-as="ordinal">10</say-as> in line.
    Or I can even speak in digits. The digits for ten are <say-as interpret-as="characters">10</say-as>.
    I can also substitute phrases, like the <sub alias="World Wide Web Consortium">W3C</sub>.
    Finally, I can speak a paragraph with two sentences.
    <p><s>This is sentence one.</s><s>This is sentence two.</s></p>
    </speak>"""
def tts_ssml():
    # Set the text input to be synthesized
    inp = inputtxt.get(1.0, "end-1c")
    synth = texttospeech_v1.SynthesisInput(ssml=inp)
    tts_to_mp3(synth)
def tts_text():
    # Set the text input to be synthesized
    inp = inputtxt.get(1.0, "end-1c")
    synth = texttospeech_v1.SynthesisInput(text=inp)
    tts_to_mp3(synth)
def tts_to_mp3(synthesis_input):
    voice = texttospeech_v1.VoiceSelectionParams(
        name='en-US-Wavenet-F', language_code="en-US"
    )
    # Select the type of audio file you want returned
    audio_config = texttospeech_v1.AudioConfig(
        # https://cloud.google.com/text-to-speech/docs/reference/rpc/google.cloud.texttospeech.v1#audioencoding
        audio_encoding=texttospeech_v1.AudioEncoding.LINEAR16, pitch=-2
    )
    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        voice=voice,input=synthesis_input,  audio_config=audio_config
    )
    # The response's audio_content is binary.
    file_exists = exists("output.mp3")
    if file_exists:
        os.remove("output.mp3")
    with open(r"output.mp3", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        #Shows up on screen when done writing to file
        doneTextWidget = tk.Label(frame, text = 'Audio content written to file "output.mp3"')
        doneTextWidget.config(font = ("Courier", 14))
        doneTextWidget.pack()
        print('Audio content written to file "output.mp3"')
frame = tk.Tk()
frame.title("TextBox Input")
frame.geometry('800x500')
# TextBox Creation
inputtxt = tk.Text(frame,
                   height = 20,
                   width = 75)
inputtxt.pack()
txtButton = tk.Button(frame,
                        text = "Text",
                        command = tts_text)
ssmlButton = tk.Button(frame,
                        text = "SSML",
                        command = tts_ssml)
txtButton.pack()
ssmlButton.pack()
# Label Creation
lbl = tk.Label(frame, text = "")
lbl.pack()
frame.mainloop()
#playsound("output.mp3")