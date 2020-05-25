import json
import speech_recognition as s_r
import pyttsx3


def text_to_speech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 20)
    engine.setProperty('voice', voices[2].id)
    engine.say(text)
    engine.runAndWait()


with open('Dataset.json') as json_file:
    intents = json.load(json_file)


def speech_to_text():
    try:
        r = s_r.Recognizer()
        my_mic = s_r.Microphone(device_index=1)
        with my_mic as source:
            # print("now u can talk")
            r.adjust_for_ambient_noise(source, duration=0.5)
            r.pause_threshold = 0.5 # gap between phrases
            audio = r.listen(source, timeout=2)
        x = r.recognize_google(audio, language='en-US', show_all=True)
        x = r.recognize_google(audio)
        return x
    except s_r.UnknownValueError or LookupError:
        return "I couldn't hear anything"
