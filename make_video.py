import os, random, datetime, textwrap, json
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips
import subprocess

today = datetime.datetime.now()
day = today.timetuple().tm_yday
random.seed(day)

jokes = [
  ("Ghar todne ka kaam 😂", [("Ramesh", "Bhaiya ghar todne ke liye labour chahiye."), ("Bholu", "Ye lo meri biwi ko le jao."), ("Ramesh", "Ye ghar todegi?"), ("Bholu", "Ye zubaan se hi ghar tod deti hai."), ("Ramesh", "Bhaiya aap to bade bhari aadmi ho.")]),
  ("Samosa chor 😂", [("Guddu", "Bhaiya samosa kitne ka hai?"), ("Dukan", "20 rupaye ka."), ("Guddu", "To ek kaam karo, 10 ka de do."), ("Dukan", "Aadha samosa kaise du?"), ("Guddu", "Aadha kha ke de do.")]),
  ("Ullu ban gaya 😂", [("Bholu", "Bhai tujhe ullu banaya."), ("Guddu", "Kab?"), ("Bholu", "Jab tu peeche dekh raha tha."), ("Guddu", "Peeche to koi tha hi nahi."), ("Bholu", "Tabhi to ullu ban gaya.")]),
  ("Cycle wali 😂", [("Guddu", "Bhai cycle de de."), ("Bholu", "Cycle to puncture hai."), ("Guddu", "To hawa bhar de."), ("Bholu", "Hawa to mere paas bhi nahi hai.")]),
  ("Exam wali 😂", [("Teacher", "Tum fail kaise hue?"), ("Bholu", "Sir paper mushkil tha."), ("Teacher", "To padha kyu nahi?"), ("Bholu", "Sir aapne padhaya hi nahi."), ("Teacher", "Chup kar, kal apne papa ko leke aana.")]),
]
idx = day % len(jokes)
top_text, dialogues = jokes[idx]
title = top_text + " | Guddu Bholu Comedy"
print("TITLE:", title)
os.makedirs("output",
