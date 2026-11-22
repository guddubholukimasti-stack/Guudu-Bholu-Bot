import random
from PIL import Image, ImageDraw
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip

stories = [
    ("Guddu ne Bholu se kaha aaj samosa free hai", "Bholu bhaag ke dukaan gaya, waha samosa tha hi nahi!"),
    ("Bholu ne Guddu ka samosa chura liya", "Guddu bola, mera samosa wapas de warna main ro dunga!"),
    ("Guddu bola aaj main YouTube star banunga", "Bholu bola, pehle naha ke aa, fir star baniyo!"),
]

title, punch = random.choice(stories)
text = title + ". " + punch

img = Image.new('RGB', (1080, 1920), color=(255, 193, 7))
draw = ImageDraw.Draw(img)
draw.text((80, 700), "GUDDU BHOLU", fill=(0,0,0))
draw.text((80, 800), title, fill=(0,0,0))
draw.text((80, 950), punch, fill=(100,0,0))
img.save("frame.jpg")

tts = gTTS(text=text, lang='hi')
tts.save("voice.mp3")

audio = AudioFileClip("voice.mp3")
clip = ImageClip("frame.jpg").with_duration(audio.duration).with_audio(audio)
clip.write_videofile("final_video.mp4", fps=24)
print("VIDEO BAN GAYA!")
