import speech_recognition as sr
import webbrowser
import pyttsx3
import songsLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import time
import os

recognize = sr.Recognizer()
engine = pyttsx3.init()
newsAPI = "YOUR_NEWZ_API" #add your news api here

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize the mixer module
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the MP3 file
    pygame.mixer.music.play()

    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiProcess(command):
    client = OpenAI(
        api_key="YOUR_API_KEY", #Enter you openai api key here
    )
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are a virtual assistant skilled in general tasks like Alexa and Google Cloud. Give short responses."},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = songsLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsAPI}")
        if r.status_code == 200:
            # parse the JSON requests
            data = r.json()

            # Extract the articles
            articles = data.get('articles', [])

            # print the headlines
            for article in articles:
                speak(article['title'])
    else:
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis......")

    while True:
        # Listen for the wake word Jarvis
        # obtain audio from the microphone
        r = sr.Recognizer()

        print("Recognizing....")
        # recognize speech using Google
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yeah")
                # Listen for command
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source)
                    print("Jarvis active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
        except Exception as e:
            print("error; {0}".format(e))
