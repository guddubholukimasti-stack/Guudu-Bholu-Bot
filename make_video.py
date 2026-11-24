import os, random, datetime, textwrap, json, shutil
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips

today = datetime.datetime.now()
day = today.timetuple().tm_yday
random.seed(day)
tops = "samosa|paise|ullu|cycle|cricket|train|exam|phone|jungle|mela".split("|")
stories = []
stories.append("Bholu ne samosa liya. Guddu ne kha liya. Bholu ko gussa aaya. Guddu bola sorry bhai. Dono ne milke samosa khaya. Dono haste hue ghar gaye.")
stories.append("Bholu ko paise mile. Bholu bahut khush hua. Dono ne party ki. Dono ne samosa khaya. Dono haste hue ghar gaye.")
stories.append("Guddu ne Bholu ko ullu banaya. Bholu peeche dekhne laga. Dono mela gaye. Dono ne golgappe khaye. Dono haste hue ghar gaye.")
stories.append("Bholu ne cycle tod di. Dono ne milke theek ki. Dono cycle pe ghoome. Dono haste hue ghar gaye.")
stories.append("Guddu Bholu cricket khele. Guddu ne chhakka mara. Dono ki team jeet gayi. Dono ne samosa khaya.")
stories.append("Guddu Bholu train me gaye. Bholu ko dar laga. Guddu bola dar mat. Dono haste hue ghar gaye.")
stories.append("Guddu Bholu ka exam tha. Guddu ne Bholu ko sikhaya. Dono ka exam accha gaya. Dono khush ho ke ghar gaye.")
stories.append("Bholu ne phone tod diya. Bholu bola sorry bhai. Dono ne cartoon dekha. Dono haste hue ghar gaye.")
stories.append("Guddu Bholu jungle gaye. Bholu ko sher se dar laga. Dono ne samosa khaya. Dono haste hue ghar gaye.")
stories.append("Guddu Bholu mela gaye. Dono ne jhoola jhoola. Dono ne golgappe khaye. Dono haste hue ghar gaye.")
i = day % 10
top_text = "Guddu Bholu " + tops[i] + " wali kahani"
red_word = tops[i]
story = stories[i] + " Subscribe karo."
title = top_text + " | Guddu Bholu Comedy"
print("TITLE:", title)
os.makedirs("output", exist_ok=True)
gTTS(text=story, lang="hi", slow=False).save("output/audio.mp3")
audio = AudioFileClip("output/audio.mp3")
total = audio.duration
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
fb = ImageFont.truetype(F, 62)
fs = ImageFont.truetype(F, 46)
fw = ImageFont.truetype(F, 50)
BGS = [((255,220,100),(255,180,0),"TOY SHOP"),((180,220,255),(100,160,255),"PARKING"),((200,255,200),(120,200,120),"GHAR"),((255,200,220),(255,120,180),"RESTAURANT"),((255,240,180),(200,160,80),"SCHOOL"),((220,220,255),(140,140,255),"MELA")]
random.shuffle(BGS)
def draw(d, cx, cy, col, shirt, name, talk, pose):
    y = cy + 3
    if pose == "gussa":
        y = cy + 10
    if pose == "khush":
        y = cy + 12
    d.rectangle([cx-55, y+280, cx-15, y+420], fill=(30,30,200))
    d.rectangle([cx+15, y+280, cx+55, y+420], fill=(30,30,200))
    d.rectangle([cx-110, y+80, cx+110, y+290], fill=shirt)
    d.ellipse([cx-80, y+170, cx+80, y+280], fill=shirt)
    d.ellipse([cx-130, y-170, cx+130, y+90], fill=col)
    d.ellipse([cx-65, y-70, cx-25, y-30], fill=(255,255,255))
    d.ellipse([cx+25, y-70, cx+65, y-30], fill=(255,255,255))
    d.ellipse([cx-48, y-55, cx-32, y-38], fill=(0,0,0))
    d.ellipse([cx+32, y-55, cx+48, y-38], fill=(0,0,0))
    if talk:
        d.ellipse([cx-35, y+10, cx+35, y+40], fill=(0,0,0))
    else:
        d.arc([cx-35, y+5, cx+35, y+45], 0, 180, fill=(0,0,0), width=5)
    d.text((cx-70, y+440), name, fill=(0,0,0), font=fs)
sent = [s.strip() for s in story.split(".") if len(s.strip()) > 5]
scenes = []
for k in range(6):
    p = sent[k*2:(k+1)*2]
    if len(p) == 0:
        p = [sent[-1]]
    scenes.append(". ".join(p))
clips = []
sd = total / 6
for si in range(6):
    bg = BGS[si]
    for f in range(10):
        img = Image.new("RGB", (1080,1920), bg[0])
        d = ImageDraw.Draw(img)
        d.rectangle([0,900,1080,1500], fill=bg[1])
        d.rectangle([50,500,1030,900], fill=(255,255,255))
        d.text((380,650), bg[2], fill=(0,0,0), font=fb)
        draw(d, 300, 1150, (255,180,120), (255,80,80), "GUDDU", si%2==0, "normal")
        draw(d, 780, 1150, (255,210,150), (255,220,0), "BHOLU", si%2!=0, "normal")
        d.rectangle([50,80,1030,320], fill=(255,255,255))
        yy = 110
        for line in textwrap.wrap(top_text, width=22)[:2]:
            c = (255,0,0) if red_word in line.lower() else (0,0,0)
            d.text((80, yy), line, fill=c, font=fb)
            yy = yy + 85
        d.text((320,1750), "Wait for end", fill=(0,0,0), font=fw)
        d.text((80,1650), title, fill=(255,255,255), font=fs)
        fn = "output/f_" + str(si) + "_" + str(f) + ".jpg"
        img.save(fn)
    sc = [ImageClip("output/f_"+str(si)+"_"+str(f)+".jpg").set_duration(sd/10) for f in range(10)]
    clips.append(concatenate_videoclips(sc, method="compose"))
final = concatenate_videoclips(clips, method="compose").set_audio(audio).set_duration(total)
final.write_videofile("output/final.mp4", fps=24, codec="libx264", audio_codec="aac")
print("VIDEO DONE")
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
creds = Credentials.from_authorized_user_info(json.loads(os.environ["YOUTUBE_TOKEN"]))
youtube = build("youtube", "v3", credentials=creds)
body = {"snippet": {"title": title+" #Shorts", "description": story, "tags": ["Guddu Bholu","Shorts"], "categoryId": "24"}, "status": {"privacyStatus": "public", "madeForKids": True}}
req = youtube.videos().insert(part="snippet,status", body=body, media_body=MediaFileUpload("output/final.mp4"))
print("UPLOAD HO GAYA! ID:", req.execute()["id"])
