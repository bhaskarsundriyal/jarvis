import sys
import os
import wikipedia
import threading
import webbrowser
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from training_model.model import mind
from head.mouth import speak

qa_file_path = r"C:\Users\ACER\Desktop\pyhon\jarvis\data\brain_data\qna.txt"

def load_qa_data(file_path):
    """Load QnA data from file into a dictionary."""
    qa_dict = {}
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                try:
                    q, a = line.split(":", 1) 
                    qa_dict[q.strip()] = a.strip()
                except ValueError:
                    continue  
    return qa_dict

def save_qa_data(file_path, qa_dict):
    """Save QnA dictionary to file."""
    with open(file_path, "w", encoding="utf-8") as f:
        for q, a in qa_dict.items():
            f.write(f"{q} : {a}\n")

qa_dict = load_qa_data(qa_file_path)

def print_animated_message(message):
    """Print text with typing animation effect."""
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.075)
    print()

def wiki_search(prompt):
    """Search Wikipedia, fallback to Google if no page found."""
    search_prompt = prompt.replace("jarvis", "").replace("wikipedia", "").strip()

    if not search_prompt:  # skip empty searches
        return

    try:
        wiki_summary = wikipedia.summary(search_prompt, sentences=2)

        animate_thread = threading.Thread(target=print_animated_message, args=(wiki_summary,))
        speak_thread = threading.Thread(target=speak, args=(wiki_summary,))

        animate_thread.start()
        speak_thread.start()

        animate_thread.join()
        speak_thread.join()

        qa_dict[search_prompt] = wiki_summary
        save_qa_data(qa_file_path, qa_dict)

    except wikipedia.exceptions.DisambiguationError:
        speak("There is a disambiguation page for the given query. Please provide more specific information.")
        print("There is a disambiguation page for the given query. Please provide more specific information.")

    except wikipedia.exceptions.PageError:
        google_search(prompt)

def google_search(query):
    """Fallback: open Google search in browser."""
    query = query.replace("who is ", "").strip()

    if query:
        url = "https://www.google.com/search?q=" + query
        webbrowser.open_new_tab(url)
        speak(f"You can see search results for {query} in Google on your screen.")
        print(f"You can see search results for {query} in Google on your screen.")
    else:
        speak("I didn't catch what you said.")
        print("I didn't catch what you said.")

def brain(text):
    if not text.strip():  # <-- skip empty input
        return

    try:
        response = mind(text)
        wiki_summary = wikipedia.summary(text, sentences=1)

        animate_thread = threading.Thread(target=print_animated_message, args=(wiki_summary,))
        speak_thread = threading.Thread(target=speak, args=(wiki_summary,))

        animate_thread.start()
        speak_thread.start()

        animate_thread.join()
        speak_thread.join()

        qa_dict[text] = wiki_summary
        save_qa_data(qa_file_path, qa_dict)

    except wikipedia.exceptions.DisambiguationError:
        speak("There is a disambiguation page for the given query. Please provide more specific information.")
        print("There is a disambiguation page for the given query. Please provide more specific information.")

    except wikipedia.exceptions.PageError:
        google_search(text)

# ------------------------
# Removed the call brain("") to prevent errors
# ------------------------
