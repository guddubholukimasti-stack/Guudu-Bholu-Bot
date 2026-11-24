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
            F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
fb = ImageFont.truetype(F, 58)
fs = ImageFont.truetype(F, 42)
def draw_bg():
    img = Image.new("RGB", (1080,1920), (135,206,235))
    d = ImageDraw.Draw(img)
    d.rectangle([0,1300,1080,1920], fill=(120,120,120))
    d.rectangle([0,1300,1080,1450], fill=(200,200,200))
    d.rectangle([80,700,1000,1250], fill=(255,200,0))
    d.text((150,850), "LABOUR CHOWK", fill=(0,0,180), font=fb)
    d.ellipse([100,300,600,750], fill=(0,180,0))
    d.rectangle([300,700,360,1100], fill=(120,60,0))
    d.rectangle([0,1000,1080,1300], fill=(0,150,0))
    return img, d
def draw_stick(d, cx, cy, talk):
    d.line([cx, cy+150, cx, cy+450], fill=(0,0,0), width=12)
    d.line([cx, cy+450, cx-80, cy+650], fill=(0,0,0), width=10)
    d.line([cx, cy+450, cx+80, cy+650], fill=(0,0,0), width=10)
    d.line([cx, cy+200, cx-100, cy+300], fill=(0,0,0), width=10)
    d.line([cx, cy+200, cx+100, cy+300], fill=(0,0,0), width=10)
    for k, col in enumerate([(255,0,0),(255,255,255),(255,0,0)]):
        d.rectangle([cx-70, cy+150+k*40, cx+70, cy+190+k*40], fill=col)
    d.ellipse([cx-110, cy-120, cx+110, cy+100], fill=(255,255,255), outline=(0,0,0), width=6)
    for a in range(-60, 70, 20):
        d.polygon([(cx+a, cy-100),(cx+a+10, cy-160),(cx+a+20, cy-100)], fill=(255,120,0))
    d.ellipse([cx-75, cy-50, cx-5, cy+30], fill=(255,255,255), outline=(0,0,0), width=4)
    d.ellipse([cx+5, cy-50, cx+75, cy+30], fill=(255,255,255), outline=(0,0,0), width=4)
    d.ellipse([cx-45, cy-20, cx-20, cy+5], fill=(0,0,0))
    d.ellipse([cx+20, cy-20, cx+45, cy+5], fill=(0,0,0))
    if talk:
        d.ellipse([cx-35, cy+40, cx+35, cy+75], fill=(0,0,0))
    else:
        d.arc([cx-35, cy+35, cx+35, cy+75], 0, 180, fill=(0,0,0), width=4)
def draw_man(d, cx, cy, talk):
    d.ellipse([cx-90, cy-100, cx+90, cy+100], fill=(255,210,170), outline=(0,0,0), width=4)
    d.rectangle([cx-90, cy-120, cx+90, cy-20], fill=(0,0,0))
    d.rectangle([cx-60, cy-50, cx-10, cy-10], fill=(180,230,255), outline=(0,0,0), width=3)
    d.rectangle([cx+10, cy-50, cx+60, cy-10], fill=(180,230,255), outline=(0,0,0), width=3)
    if talk:
        d.ellipse([cx-25, cy+50, cx+25, cy+70], fill=(0,0,0))
    else:
        d.arc([cx-25, cy+40, cx+25, cy+70], 0, 180, fill=(0,0,0), width=4)
    d.rectangle([cx-70, cy+120, cx+70, cy+350], fill=(200,200,255))
    d.line([cx, cy+350, cx, cy+550], fill=(0,0,0), width=10)
clips = []
for i,(who,line,c) in enumerate(audios):
    dur = c.duration
    for f in range(12):
        base,_ = draw_bg()
        d = ImageDraw.Draw(base)
        draw_stick(d, 720, 900, talk=(i%2==0))
        draw_man(d, 300, 900, talk=(i%2==1))
        d.rectangle([60,90,1020,210], fill=(255,255,255))
        d.text((90,120), top_text, fill=(0,0,0), font=fs)
        d.rectangle([330,1750,750,1850], fill=(0,0,0))
        d.text((360,1775), "wait for end 😂", fill=(255,255,255), font=fs)
        fn = f"output/f_{i}_{f}.jpg"
        base.save(fn)
    sc = [ImageClip(f"output/f_{i}_{f}.jpg").set_duration(dur/12) for f in range(12)]
    clips.append(concatenate_videoclips(sc, method="compose").set_audio(c))
final = concatenate_videoclips(clips, method="compose")
final.write_videofile("output/final.mp
                      print("VIDEO DONE")
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
creds = Credentials.from_authorized_user_info(json.loads(os.environ["YOUTUBE_TOKEN"]))
youtube = build("youtube", "v3", credentials=creds)
body = {"snippet": {"title": title+" #Shorts", "description": " ".join([l for _,l in dialogues]), "tags": ["Comedy","Shorts"], "categoryId": "24"}, "status": {"privacyStatus": "public", "madeForKids": True}}
req = youtube.videos().insert(part="snippet,status", body=body, media_body=MediaFileUpload("output/final.mp4"))
print("UPLOAD HO GAYA! ID:", req.execute()["id"])
