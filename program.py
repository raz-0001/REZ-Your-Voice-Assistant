from tkinter import *
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import os
import webbrowser
import smtplib
import sys
from PIL import Image
import urllib.request
import urllib.parse
import re


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=5)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        commands()
    return query

#set email and password
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

def wishMe():
    hour=int(datetime.datetime.now().hour)
    if(hour<=6):
        engine.say("Good Night")
        engine.runAndWait()
    elif(hour>6 and hour<=12):
        engine.say("Good Morning")
        engine.runAndWait()
    elif(hour>12 and hour<=2):
        engine.say("Good Afternoon")
        engine.runAndWait()
    else :
        engine.say("Good Evening")
        engine.runAndWait()
    engine.say("Sir,what can I do for you")
    engine.runAndWait()

def commands():
    query = takeCommand().lower()

    # Logic for executing tasks based on query
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif 'open youtube' in query:
        webbrowser.open("youtube.com")

    elif 'search' in query:
        query=query.replace("search","")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif 'open stackoverflow' in query:
        webbrowser.open("stackoverflow.com")   


    elif 'play' in query:
        query=query.replace("play","")
        query_string = urllib.parse.urlencode({f"search_query" :{query} })
        html_content = urllib.request.urlopen("https://www.youtube.com.hk/results?"+query_string)
        search_results = re.findall(r'url\"\:\"\/watch\?v\=(.*?(?=\"))', html_content.read().decode())
        if search_results:
            print("http://www.youtube.com/watch?v=" + search_results[0])
            webbrowser.open_new("http://www.youtube.com/watch?v={}".format(search_results[0]))

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")    
        speak(f"Sir, the time is {strTime}")
    
    elif 'open code' in query:
        #set path of your VS Code
        codePath = "C:\\Users\\Rajibul Khan\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(codePath)


    elif 'email to harry' in query:
        try:
            speak("What to write?")
            content = takeCommand()
            speak("Whom do you want to send?")
            to = takeCommand() 
            sendEmail(to, content)
            speak("Email has been sent!")
        except Exception as e:
            print(e)
            speak("Sorry Sir.Your mail cannot be sent!")

    elif 'my picture' in query:
        img = Image.open("magic.jpg")
        img.show()

    elif 'handsome' in query:
        file="Chhee.mp4"
        os.system(file)
    
    elif 'love me' in query:
        file="TumharaMuu.mp4"
        os.system(file)
        
    elif "exit" or "quit" in query:
        sys.exit()
        

if __name__=="__main__":

    win=Tk()
    win.title("REZ")
    win.geometry("250x250")

    b=Button(win, text="Greet Me",width=100,activebackground="green",command=wishMe)
    b.pack(pady=30)

    photo = PhotoImage(file = r"microphone.png")
  
    c=Button(win,text="Speak Now!",image=photo,height=120,width=120,activebackground="green",command=commands)
    c.pack(side=TOP)



    win.mainloop()

