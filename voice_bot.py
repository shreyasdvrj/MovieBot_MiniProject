import requests
import speech_recognition as sr     # import the library
import subprocess
from gtts import gTTS
from playsound import playsound
from translate import Translator
import datetime

# sender = input("What is your name?\n")

bot_message = ""
message=""

translator = Translator(to_lang='en')
translation = translator.translate("hello")

r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": "Hello"})

print("Bot says, ",end=' ')
for i in r.json():
    bot_message = i['text']
    print(f"{bot_message}")

myobj = gTTS(text=translator.translate(bot_message),lang='en')
date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
filename = "voice"+date_string+".mp3"
myobj.save(filename)
print('saved')
playsound(filename)
# Playing the converted file
#subprocess.call(['cvlc', "welcome.mp3", '--play-and-exit'],shell=True)

while bot_message != "bye" or bot_message!='Bye' or bot_message!='thanks':

    r = sr.Recognizer()  # initialize recognizer
    with sr.Microphone() as source:  # mention source it will be either Microphone or audio files.
        print("Speak Anything :")
        audio = r.listen(source)  # listen to the source
        try:
            message = r.recognize_google(audio)  # use recognizer to convert our audio into text part.
            translator = Translator(to_lang='en')
            print("You said : {}".format(translator.translate(message)))

        except:
            print("Sorry could not recognize your voice")  # In case of voice not recognized  clearly
    if len(message)==0:
        continue
    print("Sending message now...")

    r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": translator.translate(message)})

    print("Bot says, ",end=' ')
    for i in r.json():
        bot_message = i['text']
        print(f"{bot_message}")
    translator = Translator(to_lang='en')
    myobj = gTTS(text=translator.translate(bot_message))
    date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice"+date_string+".mp3"
    myobj.save(filename)
    playsound(filename)
    print('saved')
    # Playing the converted file
    #subprocess.call(['cvlc', "welcome.mp3", '--play-and-exit'], shell=True)
    if bot_message=='bye':
        break