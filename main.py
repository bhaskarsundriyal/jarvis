import os
import re
import shutil
import asyncio
import threading
import uuid
import edge_tts
import pygame
import speech_recognition as sr
import time
import random
import webbrowser
import wikipedia
import subprocess
import difflib

VOICE = "en-AU-WilliamNeural"
QNA_FILE = "C:/Users/ACER/Desktop/pyhon/jarvis/data/brain_data/qna.txt"

# ---------------- SPEAK ---------------- #
def remove_file(file_path):
    try:
        os.remove(file_path)
    except:
        pass

async def amain(TEXT, output_file):
    cm_txt = edge_tts.Communicate(TEXT, VOICE)
    await cm_txt.save(output_file)
    threading.Thread(target=play_audio, args=(output_file,), daemon=True).start()

def play_audio(file_path):
    try:
        pygame.mixer.init()
        sound = pygame.mixer.Sound(file_path)
        sound.play()
        while pygame.mixer.get_busy():
            pygame.time.delay(100)
        pygame.mixer.quit()
        remove_file(file_path)
    except:
        pass

def speak(TEXT):
    try:
        filename = os.path.join(os.getcwd(), f"output_{uuid.uuid4().hex}.mp3")
        asyncio.run(amain(TEXT, filename))
    except:
        pass

# ---------------- LISTEN ---------------- #
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, phrase_time_limit=6)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")  # Show text
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError:
            print("Speech service error")
            speak("Sorry, I cannot access the speech service right now.")
            return ""

# ---------------- WISH & WELCOME ---------------- #
def make_wish():
    hour = int(time.strftime("%H"))
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

def welcome():
    welcomes = ["Hello!", "Hi there!", "Welcome back!"]
    speak(random.choice(welcomes))

# ---------------- QnA ---------------- #
def load_qna(file_path=QNA_FILE):
    qna_dict = {}
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    q, a = line.strip().split(":", 1)
                    qna_dict[q.lower().strip()] = a.strip()
    return qna_dict

def save_qna(question, answer, file_path=QNA_FILE):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{question}: {answer}\n")

def answer_question(user_question, qna_dict):
    best_match = difflib.get_close_matches(user_question.lower(), qna_dict.keys(), n=1, cutoff=0.6)
    if best_match:
        return qna_dict[best_match[0]]
    return None

# ---------------- SEARCH & ACTIONS ---------------- #
KNOWN_SITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://twitter.com",
    "gmail": "https://mail.google.com",
}

def normalize_command(text):
    text = text.lower()
    text = re.sub(r'(open|launch|start|play|go to)', '', text)
    return text.strip()

def wiki_search(query):
    try:
        q = re.sub(r'(who is|what is|tell me about|define|jarvis)', '', query.lower()).strip().title()
        return wikipedia.summary(q, sentences=2)
    except:
        return None

def handle_play(command):
    text = re.sub(r'(play|music|songs?|video|by|of|on youtube|on spotify)', '', command, flags=re.I).strip()
    if not text:
        speak("What do you want me to play?")
        return
    url = "https://www.youtube.com/results?search_query=" + "+".join(text.split())
    webbrowser.open_new_tab(url)
    speak(f"Searching {text} on YouTube.")

def handle_open(command):
    target = normalize_command(command)
    if not target:
        return

    # Windows built-ins
    if "setting" in target:
        os.system("start ms-settings:")
        return
    if "my pc" in target or "this pc" in target or "explorer" in target:
        os.system("explorer shell:MyComputerFolder")
        return
    if "control" in target and "panel" in target:
        os.system("control")
        return

    # Known websites
    if target in KNOWN_SITES:
        webbrowser.open_new_tab(KNOWN_SITES[target])
        return

    # Try PATH executables
    exe_name = target.replace(" ", "") + ".exe"
    path = shutil.which(exe_name) or shutil.which(target)
    if path:
        subprocess.Popen(path)
        return

    # Check common install locations dynamically (Program Files & AppData)
    possible_dirs = [
        os.environ.get("ProgramFiles", r"C:\Program Files"),
        os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
        os.path.join(os.environ.get("LOCALAPPDATA", r"C:\Users\%USERNAME%\AppData\Local")),
    ]
    variants = [target + ".exe", target.replace(" ", "") + ".exe", target.capitalize() + ".exe"]
    for dir_ in possible_dirs:
        for var in variants:
            exe_path = os.path.join(dir_, var)
            if os.path.exists(exe_path):
                subprocess.Popen(exe_path)
                return

    # Silent fallback to Google search
    webbrowser.open_new_tab(f"https://www.google.com/search?q={'+'.join(target.split())}")

def system_command(cmd):
    try:
        if cmd == "shutdown": os.system("shutdown /s /t 5")
        elif cmd == "restart": os.system("shutdown /r /t 5")
        elif cmd == "lock": os.system("rundll32.exe user32.dll,LockWorkStation")
        elif cmd == "logout": os.system("shutdown /l")
    except:
        pass

# ---------------- MAIN JARVIS ---------------- #
def jarvis():
    make_wish()
    welcome()
    qna_dict = load_qna()

    while True:
        user_input = listen()
        if not user_input: continue
        command = user_input.lower().strip()

        if command in ["exit", "quit", "stop", "goodbye"]:
            speak("Goodbye!")
            break

        # System commands
        for sys_cmd in ["shutdown", "restart", "lock", "logout"]:
            if sys_cmd in command:
                system_command(sys_cmd)
                break

        # Play music
        if command.startswith("play"):
            handle_play(command)
            continue

        # Open apps/websites
        if command.startswith(("open", "launch", "start")):
            handle_open(command)
            continue

        # QnA
        response = answer_question(user_input, qna_dict)
        if response:
            speak(response)
        else:
            wiki_answer = wiki_search(user_input)
            if wiki_answer:
                speak(wiki_answer)
                save_qna(user_input, wiki_answer)
                qna_dict[user_input.lower()] = wiki_answer
            else:
                # Silent fallback to Google
                webbrowser.open_new_tab(f"https://www.google.com/search?q={'+'.join(user_input.split())}")

if __name__ == "__main__":
    jarvis()
