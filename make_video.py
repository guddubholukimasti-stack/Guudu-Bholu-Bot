import os
import random
import datetime
import textwrap
import json
import subprocess
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

today = datetime.datetime.now()
day_num = today.timetuple().tm_yday
random.seed(day_num)
print("Aaj:", today.strftime("%d %b"))

def get_story():
    s1 = "Ek din Guddu aur Bholu mela gaye. "
    s1 += "Bholu ne samosa liya. "
    s1 += "Guddu ne chupke se kha liya. "
    s1 += "Bholu ko gussa aa gaya. "
    s1 += "Guddu bola sorry bhai. "
    s1 += "Dono ne milke samosa khaya. "
    s1 += "Dono haste hue ghar gaye."
    s2 = "Ek din Bholu ko paise mile. "
    s2 += "Bholu bahut khush hua. "
    s2 += "Dono ne party ki. "
    s2 += "Dono ne samosa khaya. "
    s2 += "Dono haste hue ghar gaye."
    s3 = "Ek din Guddu ne Bholu ko ullu banaya. "
    s3 += "Bholu peeche dekhne laga. "
    s3 += "Dono mela gaye. "
    s3 += "Dono ne golgappe khaye. "
    s3 += "Dono haste hue ghar gaye."
    s4 = "Ek din Bholu ne cycle tod di. "
    s4 += "Dono ne milke theek ki. "
    s4 += "Dono cycle pe ghoome. "
    s4 += "Dono haste hue ghar gaye."
    s5 = "Ek din Guddu Bholu cricket khele. "
    s5 += "Guddu ne chhakka mara. "
    s5 += "Dono ki team jeet gayi. "
    s5 += "Dono ne samosa khaya."
    s6 = "Ek din Guddu Bholu train me gaye. "
    s6 += "Bholu ko dar laga. "
    s6 += "Guddu bola dar mat. "
    s6 += "Dono haste hue ghar gaye."
    s7 = "Ek din Guddu Bholu ka exam tha. "
    s7 += "Guddu ne Bholu ko sikhaya. "
    s7 += "Dono ka exam accha gaya. "
    s7 += "Dono khush ho ke ghar gaye."
    s8 = "Ek din Bholu ne phone tod diya. "
    s8 += "Bholu bola sorry bhai. "
    s8 += "Dono ne cartoon dekha. "
    s8 += "Dono haste hue ghar gaye."
    s9 = "Ek din Guddu Bholu jungle gaye. "
    s9 += "Bholu ko sher se dar laga. "
    s9 += "Dono ne samosa khaya. "
    s9 += "Dono haste hue ghar gaye."
    s10 = "Ek din Guddu Bholu mela gaye. "
    s10 += "Dono ne jhoola jhoola. "
    s10 += "Dono ne golgappe khaye. "
    s10 += "Dono haste hue ghar gaye."
    tops = []
    tops.append("Guddu ne Bholu ka samosa kha liya")
    tops.append("Bholu ko paise mile")
    tops.append("Guddu ne Bholu ko ullu banaya")
    tops.append("Bholu ne cycle tod di")
    tops.append("Guddu Bholu ka cricket match")
    tops.append("Guddu Bholu train me fas gaye")
    tops.append("Guddu Bholu ka exam wala din")
    tops.append("Bholu ne phone tod diya")
    tops.append("Guddu Bholu ka jungle safar")
    tops.append("Guddu Bholu ki mela masti")
    reds = []
    reds.append("samosa")
    reds.append("paise")
    reds.append("ullu")
    reds.append("cycle")
    reds.append("cricket")
    reds.append("train")
    reds.append("exam")
    reds.append("phone")
    reds.append("jungle")
    reds.append("mela")
    alls = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
    idx = day_num % 10
    top = tops[idx]
    red = reds[idx]
    story = alls[idx]
    story = story + " Subscribe karo."
    title = top + " | Guddu Bholu Comedy"
    return title, top, red, story

title, top_text, red_word, story = get_story()
print("TITLE:", title)

from gtts import gTTS
from moviepy.editor import AudioFileClip
os.makedirs("output", exist_ok=True)
gTTS(text=story, lang="hi", slow=False).save("output/a1.mp3")
cmd = "ffmpeg -y -i output/a1.mp3 "
cmd += "-filter:a asetrate=44100*1.25,aresample=44100,atempo=0.95 "
cmd += "output/audio.mp3"
subprocess.run(cmd, shell=True, check=True)
dur = AudioFileClip("output/audio.mp3").duration
print("Audio:", dur)

W = 1080
H = 1920
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
try:
    fb = ImageFont.truetype(F, 62)
    fs = ImageFont.truetype(F, 46)
    fw = ImageFont.truetype(F, 50)
except:
    fb = ImageFont.load_default()
    fs = fb
    fw = fb

BGS = []
BGS.append(((255, 220, 100), (255, 180, 0), "TOY SHOP"))
BGS.append(((180, 220, 255), (100, 160, 255), "PARKING"))
BGS.append(((200, 255, 200), (120, 200, 120), "GHAR"))
BGS.append(((255, 200, 220), (255, 120, 180), "RESTAURANT"))
BGS.append(((255, 240, 180), (200, 160, 80), "SCHOOL"))
BGS.append(((220, 220, 255), (140, 140, 255), "MELA"))
random.shuffle(BGS)

def get_pose(t):
    t = t.lower()
    if "gussa" in t:
        return "gussa"
    if "sorry" in t:
        return "sorry"
    if "samosa" in t:
        return "kha"
    if "dar" in t:
        return "dar"
    if "khush" in t:
        return "khush"
    if "bola" in t:
        return "bol"
    return "normal"

def draw_body(d, cx, cy, col, shirt, name, talk, pose):
    if talk == False:
        pose = "normal"
    y = cy + 3
    lean = 0
    if pose == "gussa":
        y = cy + 10
        lean = 15
    if pose == "dar":
        y = cy + 6
        lean = -10
    if pose == "khush":
        y = cy + 12
    cx = cx + lean
    x1 = cx - 55
    x2 = cx - 15
    y1 = y + 280
    y2 = y + 420
    d.rectangle([x1, y1, x2, y2], fill=(30, 30, 200))
    x1 = cx + 15
    x2 = cx + 55
    d.rectangle([x1, y1, x2, y2], fill=(30, 30, 200))
    x1 = cx - 110
    x2 = cx + 110
    y1 = y + 80
    y2 = y + 290
    d.rectangle([x1, y1, x2, y2], fill=shirt)
    x1 = cx - 80
    x2 = cx + 80
    y1 = y + 170
    y2 = y + 280
    d.ellipse([x1, y1, x2, y2], fill=shirt)
    if pose == "gussa":
        x1 = cx - 160
        x2 = cx - 100
        y1 = y + 200
        y2 = y + 260
        d.ellipse([x1, y1, x2, y2], fill=col)
        x1 = cx + 100
        x2 = cx + 160
        d.ellipse([x1, y1, x2, y2], fill=col)
    if pose == "sorry":
        x1 = cx - 30
        x2 = cx + 30
        y1 = y + 130
        y2 = y + 210
        d.ellipse([x1, y1, x2, y2], fill=col)
    if pose == "kha":
        x1 = cx + 80
        x2 = cx + 140
        y1 = y + 0
        y2 = y + 70
        d.ellipse([x1, y1, x2, y2], fill=col)
    if pose == "khush":
        x1 = cx - 170
        x2 = cx - 110
        y1 = y + 0
        y2 = y + 90
        d.ellipse([x1, y1, x2, y2], fill=col)
        x1 = cx + 110
        x2 = cx + 170
        d.ellipse([x1, y1, x2, y2], fill=col)
    if pose == "dar":
        x1 = cx - 160
        x2 = cx - 100
        y1 = y - 20
        y2 = y + 70
        d.ellipse([x1, y1, x2, y2], fill=col)
        x1 = cx + 100
        x2 = cx + 160
        d.ellipse([x1, y1, x2, y2], fill=col)
    if pose == "bol":
        x1 = cx + 110
        x2 = cx + 190
        y1 = y + 80
        y2 = y + 150
        d.ellipse([x1, y1, x2, y2], fill=col)
    if pose == "normal":
        x1 = cx - 150
        x2 = cx - 100
        y1 = y + 120
        y2 = y + 220
        d.ellipse([x1, y1, x2, y2], fill=col)
        x1 = cx + 100
        x2 = cx + 150
        d.ellipse([x1, y1, x2, y2], fill=col)
    x1 = cx - 130
    x2 = cx + 130
    y1 = y - 170
    y2 = y + 90
    d.ellipse([x1, y1, x2, y2], fill=col)
    x1 = cx - 65
    x2 = cx - 25
    y1 = y - 70
    y2 = y - 30
    d.ellipse([x1, y1, x2, y2], fill=(255, 255, 255))
    x1 = cx + 25
    x2 = cx + 65
    d.ellipse([x1, y1, x2, y2], fill=(255, 255, 255))
    x1 = cx - 48
    x2 = cx - 32
    y1 = y - 55
    y2 = y - 38
    d.ellipse([x1, y1, x2, y2], fill=(0, 0, 0))
    x1 = cx + 32
    x2 = cx + 48
    d.ellipse([x1, y1, x2, y2], fill=(0, 0, 0))
    if talk == True:
        x1 = cx - 35
        x2 = cx + 35
        y1 = y + 10
        y2 = y + 40
        d.ellipse([x1, y1, x2, y2], fill=(0, 0, 0))
    else:
        x1 = cx - 35
        x2 = cx + 35
        y1 = y + 5
        y2 = y + 45
        d.arc([x1, y1, x2, y2], 0, 180, fill=(0, 0, 0), width=5)
    d.text((cx - 70, y + 440), name, fill=(0, 0, 0), font=fs)

sent = story.split(".")
sent2 = []
for s in sent:
    s = s.strip()
    if len(s) > 5:
        sent2.append(s)
scenes = []
for i in range(6):
    p = sent2[i*2:(i+1)*2]
    if len(p) == 0:
        p = [sent2[-1]]
    scenes.append(". ".join(p))

from moviepy.editor import ImageClip
from moviepy.editor import concatenate_videoclips
audio = AudioFileClip("output/audio.mp3")
total = audio.duration
sd = total / 6
clips = []
for si in range(6):
    scene_text = scenes[si]
    bg = BGS[si]
    bg_col = bg[0]
    gr_col = bg[1]
    label = bg[2]
    for f in range(10):
        img = Image.new("RGB", (W, H), bg_col)
        d = ImageDraw.Draw(img)
        d.rectangle([0, 900, W, 1500], fill=gr_col)
        d.rectangle([50, 500, 1030, 900], fill=(255, 255, 255))
        d.text((380, 650), label, fill=(0, 0, 0), font=fb)
        pose = get_pose(scene_text)
        t1 = si % 2 == 0
        t2 = si % 2 != 0
        draw_body(d, 300, 1150, (255, 180, 120), (255, 80, 80), "GUDDU", t1, pose)
        draw_body(d, 780, 1150, (255, 210, 150), (255, 220, 0), "BHOLU", t2, pose)
        lines = textwrap.wrap(top_text, width=22)
        d.rectangle([50, 80, 1030, 320], fill=(255, 255, 255))
        yy = 110
        for line in lines[:2]:
            if red_word in line.lower():
                d.text((80, yy), line, fill=(255, 0, 0), font=fb)
            else:
                d.text((80, yy), line, fill=(0, 0, 0), font=fb)
            yy = yy + 85
        d.text((320, 1750), "Wait for end", fill=(0, 0, 0), font=fw)
        d.text((80, 1650), title, fill=(255, 255, 255), font=fs)
        fn = "output/f_" + str(si) + "_" + str(f) + ".jpg"
        img.save(fn)
    sc = []
    for f in range(10):
        fn = "output/f_" + str(si) + "_" + str(f) + ".jpg"
        c = ImageClip(fn).set_duration(sd / 10)
        sc.append(c)
    clips.append(concatenate_videoclips(sc, method="compose"))

final = concatenate_videoclips(clips, method="compose")
final = final.set_audio(audio)
final = final.set_duration(total)
final.write_videofile("output/final.mp4", fps=24, codec="libx264", audio_codec="aac")
print("VIDEO DONE")

print("Uploading...")
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
token_info = json.loads(os.environ["YOUTUBE_TOKEN"])
creds = Credentials.from_authorized_user_info(token_info)
youtube = build("youtube", "v3", credentials=creds)
body = {}
snip = {}
snip["title"] = title + " #Shorts"
snip["description"] = story + " #Shorts #GudduBholu #Comedy"
snip["tags"] = ["Guddu Bholu", "Shorts", "Hindi Kahani"]
snip["categoryId"] = "24"
body["snippet"] = snip
stat = {}
stat["privacyStatus"] = "public"
stat["madeForKids"] = True
body["status"] = stat
media = MediaFileUpload("output/final.mp4")
req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
resp = req.execute()
print("UPLOAD HO GAYA! ID:", resp["id"])
