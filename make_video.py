import random, os, json, textwrap
from PIL import Image, ImageDraw
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

stories = [
    ("Guddu: Aaj samosa free hai!", "Bholu: Bhag bhai, jaldi chal!"),
    ("Bholu: Tera samosa maine kha liya!", "Guddu: Wapas de warna ro dunga!"),
    ("Guddu: Aaj main star banunga!", "Bholu: Pehle naha ke aa bhai!"),
]
title, punch = random.choice(stories)
text = title + " " + punch

W, H = 1080, 1920
# --- BACKGROUND ---
bg = Image.new('RGB', (W, H), color=(135, 206, 235))
d = ImageDraw.Draw(bg)
d.ellipse([850, 80, 1010, 240], fill=(255, 255, 0), outline=(255, 200, 0), width=5)
d.ellipse([100, 150, 280, 230], fill=(255,255,255))
d.ellipse([200, 130, 380, 220], fill=(255,255,255))
d.rectangle([0, 1550, W, H], fill=(34, 139, 34))
d.rectangle([0, 1550, W, 1580], fill=(100, 200, 100))
bg.save("bg.jpg")

# --- CARTOON BANANE KA FUNCTION ---
def make_character(body_color, shirt, name):
    im = Image.new('RGBA', (400, 500), (0,0,0,0))
    dr = ImageDraw.Draw(im)
    dr.ellipse([50, 0, 350, 300], fill=body_color, outline=(0,0,0), width=6)
    dr.ellipse([110, 90, 170, 150], fill=(255,255,255))
    dr.ellipse([230, 90, 290, 150], fill=(255,255,255))
    dr.ellipse([128, 108, 152, 132], fill=(0,0,0))
    dr.ellipse([248, 108, 272, 132], fill=(0,0,0))
    dr.arc([120, 170, 280, 260], 0, 180, fill=(0,0,0), width=6)
    dr.rectangle([130, 300, 270, 460], fill=shirt, outline=(0,0,0), width=4)
    dr.text((130, 470), name, fill=(255,255,255))
    im.save(name + ".png")
    return name + ".png"

guddu_png = make_character((255, 193, 7), (0, 120, 255), "GUDDU")
bholu_png = make_character((255, 180, 180), (255, 50, 50), "BHOLU")

# --- SPEECH BUBBLE WALA FRAME ---
bubble = Image.new('RGBA', (W, 500), (0,0,0,0))
db = ImageDraw.Draw(bubble)
db.rounded_rectangle([50, 20, W-50, 480], radius=50, fill=(255,255,255), outline=(0,0,0), width=5)
db.text((90, 70), "\n".join(textwrap.wrap(title, width=28)), fill=(0,0,0))
db.text((90, 250), "\n".join(textwrap.wrap(punch, width=28)), fill=(200,0,0))
bubble.save("bubble.png")

# --- AUDIO ---
tts = gTTS(text=text, lang='hi')
tts.save("voice.mp3")
audio = AudioFileClip("voice.mp3")
dur = audio.duration

# --- MOTION ---
bg_clip = ImageClip("bg.jpg").with_duration(dur).resized(lambda t: 1 + 0.03*t/dur)
guddu_clip = ImageClip(guddu_png).with_duration(dur).resized(0.85).with_position(lambda t: (100, 1050 + int(30*abs(__import__('math').sin(t*4)))))
bholu_clip = ImageClip(bholu_png).with_duration(dur).resized(0.85).with_position(lambda t: (600, 1050 + int(30*abs(__import__('math').cos(t*4)))))
bubble_clip = ImageClip("bubble.png").with_duration(dur).with_position((0, 350))

final = CompositeVideoClip([bg_clip, guddu_clip, bholu_clip, bubble_clip], size=(W, H)).with_audio(audio)
final.write_videofile("final_video.mp4", fps=24)
print("VIDEO BAN GAYA!")

# --- UPLOAD ---
token_info = json.loads(os.environ["YOUTUBE_TOKEN"])
creds = Credentials.from_authorized_user_info(token_info)
youtube = build("youtube", "v3", credentials=creds)
req = youtube.videos().insert(
    part="snippet,status",
    body={"snippet": {"title": title + " | Guddu Bholu Comedy Shorts", "description": punch + "\n\n#shorts #guddu #bholu #comedy #cartoon", "categoryId": "23"}, "status": {"privacyStatus": "public"}},
    media_body=MediaFileUpload("final_video.mp4")
)
print("UPLOAD HO GAYA!", req.execute()["id"])
