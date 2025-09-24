import speech_recognition as sr
import os
import threading
from mtranslate import translate
from colorama import Fore, Style, init

init(autoreset=True)


def print_loop():
    while True:
        print(Fore.LIGHTGREEN_EX + "I AM listening.." + Style.RESET_ALL, end="\r", flush=True)

def tran_hindi_to_english(txt):
    english_txt = translate(txt, to_language="en")
    return english_txt

def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 35000
    recognizer.dynamic_energy_adjustment_damping = 0.03
    recognizer.dynamic_energy_ratio = 1.9
    recognizer.pause_threshold = 1.0       
    recognizer.non_speaking_duration = 0.5 

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recognizer.listen(source, timeout=None)
                print("\n" + Fore.LIGHTYELLOW_EX + "Got it, Vashu recognizing..." + Style.RESET_ALL, flush=True)

                recognizer_txt = recognizer.recognize_google(audio).lower()

                if recognizer_txt:
                    translate_txt = tran_hindi_to_english(recognizer_txt)
                    print(Fore.BLUE + " vashu : " + translate_txt + Style.RESET_ALL)
                else:
                    print(Fore.RED + "No speech detected." + Style.RESET_ALL)

            except sr.UnknownValueError:
                print(Fore.RED + "Could not understand audio." + Style.RESET_ALL)
            except sr.RequestError as e:
                print(Fore.RED + f"Could not request results; {e}" + Style.RESET_ALL)



os.system("cls" if os.name == "nt" else "clear")


listen_thread = threading.Thread(target=listen, daemon=True)
print_thread = threading.Thread(target=print_loop, daemon=True)

listen_thread.start()
print_thread.start()


listen_thread.join()
print_thread.join()
