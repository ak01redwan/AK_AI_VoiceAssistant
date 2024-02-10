import speech_recognition as sr
import pyperclip
import pyttsx4
import openai
import os

# here we initialize client object from OpenAI and pass our api key
# --you can change it and get one from the openai website or just use this--
client = openai.OpenAI(api_key="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")

# here we initialize the TTS engine
tts_engine = pyttsx4.init()
rate = tts_engine.getProperty('rate')
tts_engine.setProperty('rate', rate - 50)      # slower speech rate
voices = tts_engine.getProperty('voices')      # extracting the voices array
# here we can change the index to get voices for like: 0 for male voice or 1 for female voice
tts_engine.setProperty('voice', voices[0].id) 

def speak(text):
    """here we are using pyttsx4 to convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    """here we are using SpeechRecognition to listen for the commands."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        try:
            # start offline recognition
            audio = r.listen(source)
            command = r.recognize_sphinx(audio)
            print(f"Command received: {command}")
        except sr.UnknownValueError:
            speak("Sorry sir, I did not understand that.")
            return None
        except sr.RequestError as e:
            speak("Sir, there is a request error {0}".format(e))
            print(e)
            return None
        except KeyboardInterrupt:
            speak("Script has been stopped by the user from the keyboard.")
            return "AK stop"
        return command

def process_command(command):
    print(command)
    """here we process the command."""
    if "ak" or "AK" in command:
        # first of all we need to remove the word 'AK' from the command
        command_text = command.replace("AK", "", 1).strip()
        # here we send the command_text to OpenAI's API using our client object
        speak(f"Executing command {command_text}")
        # text-davinci-003 is other model we can try
        completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": command_text}])
        ai_text = completion.choices[0].message.content
        print(ai_text)
        pyperclip.copy(ai_text)
        speak(ai_text)
        # if "till" in command: 
        #     speak(ai_text)

# the main loop
while True:
    command = listen()
    if command:
        if "stop" in command:
            speak("AK assistant system is Shutting Down.")
            break
        else:
            process_command(command)
    