from head.mouth import speak
from dig_data.dig import welcome_wishes  # make sure this exists
import random

def welcome():
    """Pick a random greeting and speak it"""
    msg = random.choice(welcome_wishes)  # use a different variable name
    try:
        speak(msg)
    except Exception as e:
        print(f"[Speak Error] {e}")
    print(msg)   # optional, to see the text
    return msg
