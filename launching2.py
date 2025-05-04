import webbrowser
import pyaudio
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import os
import smtplib

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    """Convert text to speech."""
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def get_current_hour():
    """Return the current hour as an integer."""
    return int(datetime.datetime.now().hour)

def wish_user():
    """Wish the user based on the current time."""
    hour = get_current_hour()
    greeting = "Good Evening!"
    if 0 <= hour < 12:
        greeting = "Good Morning!"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon!"
    speak(greeting)
    speak("I am Jarvis, your assistant. Please tell me how may I help you today.")

def recognize_speech():
    """Capture user's voice input and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.pause_threshold = 1
        audio_input = recognizer.listen(source)

    try:
        print("Processing your input...")
        command = recognizer.recognize_google(audio_input, language='en-in')
        print(f"You said: {command}")
    except sr.UnknownValueError:
        print("Could not understand audio")
        speak("I didn't catch that. Please say that again.")
        return "None"
    except sr.RequestError as e:
        print(f"Google service error: {e}")
        speak("Sorry, I'm having trouble connecting to the speech service.")
        return "None"

    return command.lower()

def search_wikipedia(query):
    """Search and speak results from Wikipedia."""
    speak("Searching Wikipedia...")
    topic = query.replace("wikipedia", "").strip()
    try:
        summary = wikipedia.summary(topic, sentences=2)
        speak("According to Wikipedia:")
        print(summary)
        speak(summary)
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't find any results.")

def open_website(site_name):
    """Open a website based on the command."""
    websites = {
        'youtube': 'https://youtube.com',
        'google': 'https://google.com',
        'stackoverflow': 'https://stackoverflow.com'
    }
    if site_name in websites:
        speak(f"Opening {site_name}")
        webbrowser.open(websites[site_name])
    else:
        speak("Website not recognized.")

def play_music(music_directory):
    """Play the first song in the provided music directory."""
    if not os.path.exists(music_directory):
        speak("The specified music directory does not exist.")
        return
    songs = os.listdir(music_directory)
    if not songs:
        speak("No songs found in the directory.")
        return
    song_to_play = os.path.join(music_directory, songs[0])
    speak(f"Playing music: {songs[0]}")
    os.startfile(song_to_play)

def tell_time():
    """Speak the current time."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {current_time}")

def open_application(app_path):
    """Open an application using the specified path."""
    if os.path.exists(app_path):
        os.startfile(app_path)
        speak("Launching application.")
    else:
        speak("The application path seems invalid.")

def send_email(receiver_email, email_content):
    """Send an email via SMTP."""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('youremail@gmail.com', 'your-password')  # Use environment variables for safety
        server.sendmail('youremail@gmail.com', receiver_email, email_content)
        server.quit()
        speak("Email has been successfully sent.")
    except Exception as e:
        print(e)
        speak("Sorry, I was unable to send the email.")

if __name__ == "__main__":
    wish_user()
    while True:
        query = recognize_speech()

        if 'wikipedia' in query:
            search_wikipedia(query)

        elif 'open youtube' in query:
            open_website('youtube')

        elif 'open google' in query:
            open_website('google')

        elif 'open stack overflow' in query:
            open_website('stackoverflow')

        elif 'play music' in query:
            music_dir = "D:\\Music"  # Modify with a real path
            play_music(music_dir)

        elif 'the time' in query:
            tell_time()

        elif 'open code' in query:
            codePath = "C:\\Users\\User\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            open_application(codePath)

        elif 'email to me' in query:
            speak("What should I say?")
            content = recognize_speech()
            to_email = "Xyz@gmail.com"
            send_email(to_email, content)