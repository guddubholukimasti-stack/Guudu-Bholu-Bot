import os, random
import textwrap, math, json
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# 1. KAHANI
def get_new_story():
    t = ["Samosa","Mela"]
    t += ["Cricket","Train"]
    t += ["Jungle","Exam"]
    topic = random.choice(t)
    a = "Ek din Guddu aur "
    a += "Bholu ghoomne gaye. "
    a += "Dono ne bahut masti ki. "
    b = "Bholu ne gadbad ki "
    b += "aur sab hasne lage. "
    b += "Guddu ne sab sambhal liya. "
    c = "Phir dono ne samosa "
    c += "khaya aur mela dekha. "
    c += "Dono bahut khush hue. "
    d = "Tabhi tez barish aayi "
    d += "aur dono bheeg gaye. "
    d += "Dono ghar ki taraf bhage. "
    e = "Guddu ne bola himmat "
    e += "rakh, sab thik hoga. "
    e += "Bholu ne bola tu best hai. "
    f = "Aakhir me dono haste "
    f += "hue ghar gaye. "
    f += "Mummy ko kahani sunayi. "
    story = a + b + c + d + e + f
    story += " Subscribe karo."
    title = "Guddu Bholu Ka "
    title += topic + " Wala Kamaal"
    return title, story

title, story = get_new_story()
print("TITLE:", title)
print("Words:", len(story.split()))

# 2. AUDIO 1 MIN PAKKA
from gtts import gTTS
from moviepy.editor import AudioFileClip
os.makedirs("output", exist_ok=True)
audio_text = story
for _ in range(3):
    gTTS(
        text=audio_text,
        lang='hi',
        slow=True
    ).save("output/audio.mp3")
    d = AudioFileClip(
        "output/audio.mp3"
    ).duration
    print("Audio:", d)
    if d >= 60:
        break
    audio_text = audio_text + " " + story
print("Audio ban gaya")

# 3. VIDEO
W, H = 1080, 1920
F = "/usr/share/fonts"
F += "/truetype/dejavu/"
F += "DejaVuSans-Bold.ttf"
try:
    font_big = ImageFont.truetype(F, 70)
    font_small = ImageFont.truetype(F, 48)
except:
    font_big = ImageFont.load_default()
    font_small = font_big

def draw_cartoon(d, cx, cy, col, name, fr, talk):
    y = cy + int(math.sin(fr*0.5)*15)
    d.ellipse(
        [cx-110, y-100, cx+110, y+100],
        fill=col, outline=(0,0,0), width=6
    )
    d.ellipse(
        [cx-50, y-40, cx-10, y],
        fill=(255,255,255),
        outline=(0,0,0), width=3
    )
    d.ellipse(
        [cx+10, y-40, cx+50, y],
        fill=(255,255,255),
        outline=(0,0,0), width=3
    )
    d.ellipse([cx-35, y-25, cx-20, y-10], fill=(0,0,0))
    d.ellipse([cx+20, y-25, cx+35, y-10], fill=(0,0,0))
    if talk:
        mh = 20 + int(math.sin(fr*0.8)*20)
        d.ellipse([cx-30, y+30, cx+30, y+30+mh], fill=(0,0,0))
    else:
        d.arc([cx-30, y+20, cx+30, y+60], 0, 180, fill=(0,0,0), width=5)
    d.text((cx-70, y+130), name, fill=(0,0,0), font=font_small)

sent = [s.strip() for s in audio_text.split(".") if len(s.strip())>5]
scenes = []
for i in range(6):
    p = sent[i*2:(i+1)*2]
    if not p:
        p = [sent[-1]]
    scenes.append(". ".join(p))

from moviepy.editor import ImageClip
from moviepy.editor import concatenate_videoclips
audio = AudioFileClip("output/audio.mp3")
total_dur = audio.duration
print("Duration:", total_dur)
scene_dur = total_dur / 6
clips = []
for si, scene_text in enumerate(scenes):
    for f in range(10):
        img = Image.new("RGB", (W,H), (135,206,235))
        d = ImageDraw.Draw(img)
        d.rectangle([0,1400,W,H], fill=(34,139,34))
        d.rectangle([100,900,980,1400], fill=(255,210,0))
        draw_cartoon(d, 300, 1150, (255,100,100), "GUDDU", f+si*10, si%2==0)
        draw_cartoon(d, 780, 1150, (100,200,255), "BHOLU", f+si*10, si%2!=0)
        lines = textwrap.wrap(scene_text, width=22)
        y = 150
        d.rectangle([50,100,1030,100+len(lines)*90+40], fill=(255,255,255), outline=(0,0,0), width=4)
        for line in lines[:3]:
            d.text((80, y), line, fill=(0,0,0), font=font_big)
            y += 90
        d.text((80,1650), title+" #Shorts", fill=(255,255,255), font=font_small, stroke_width=2, stroke_fill=(0,0,0))
        img.save(f"output/frame_{si}_{f}.jpg")
    sc = [ImageClip(f"output/frame_{si}_{f}.jpg").set_duration(scene_dur/10) for f in range(10)]
    clips.append(concatenate_videoclips(sc, method="compose"))

final = concatenate_videoclips(clips, method="compose").set_audio(audio).set_duration(total_dur)
final.write_videofile("output/final.mp4", fps=24, codec="libx264", audio_codec="aac")
print(f"VIDEO DONE - {total_dur} sec")

# 4. UPLOAD
print("Uploading...")
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
token_info = json.loads(os.environ["YOUTUBE_TOKEN"])
creds = Credentials.from_authorized_user_info(token_info)
youtube = build("youtube", "v3", credentials=creds)
req = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": title+" #Shorts",
            "description": story[:4000]+"\n\n#Shorts #GudduBholu",
            "tags": ["Guddu Bholu","Shorts","Hindi Kahani"],
            "categoryId": "24"
        },
        "status": {
            "privacyStatus": "public",
            "madeForKids": True
        }
    },
    media_body=MediaFileUpload("output/final.mp4")
)
resp = req.execute()
print(f"UPLOAD HO GAYA! ID: {resp['id']}")
