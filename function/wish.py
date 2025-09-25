
# function/wish.py
from datetime import datetime
from head.mouth import speak
from dig_data.dig import  (
    good_morning_wishes,
    good_afternoon_wishes,
    good_night_wishes
)
from function.welcome import welcome
import random

def make_wish():
    welcome()
    hour = datetime.now().hour
    print("Test Message")
    if 5 <= hour < 12:
        msg = random.choice(good_morning_wishes)
    elif 12 <= hour < 17:
        msg = random.choice(good_afternoon_wishes)
    else:
        msg = random.choice(good_night_wishes)

    speak(msg)
   
