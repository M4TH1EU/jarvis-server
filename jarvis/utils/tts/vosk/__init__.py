import json
import os
import wave

from vosk import Model, KaldiRecognizer, SetLogLevel

from jarvis import get_path_file

SetLogLevel(-1)
model, rec = None, None


def loadModel():
    global model, rec
    if not os.path.exists("model"):
        print(
            "Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit(1)

    print("Loading model...")
    model = Model("model")
    rec = KaldiRecognizer(model, 16000)
    rec.SetWords(True)
    print("Model loaded successfully.")


def process_audio_file(file):
    global model, rec
    print("File : " + file)
    wf = wave.open(file, "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        exit(1)

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            pass
            # print(rec.Result())
        else:
            pass
            # print(rec.PartialResult())

    print(json.loads(rec.FinalResult())['text'])


if __name__ == '__main__':
    loadModel()

    path = os.path.dirname(get_path_file.__file__) + "\\audio_samples\\"
    files = ["test_jarvis_examples_french.wav"]

    for file in files:
        process_audio_file(path + file)
