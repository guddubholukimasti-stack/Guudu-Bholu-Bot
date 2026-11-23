import os, random, textwrap, datetime, math, json
from PIL import Image, ImageDraw, ImageFont

# 1. KAHANI - NAYA google.genai - 6 KEY ROTATION
def get_new_story():
    from google import genai
    all_keys = []
    for suffix in ["", "_1", "_2", "_3", "_4", "_5"]:
        k = os.environ.get(f"GEMINI_API_KEY{suffix}")
        if k and k not in all_keys:
            all_keys.append(k)
    print(f"Total Keys Mili: {len(all_keys)}")
    if not all_keys:
        raise Exception("no key")
    topics = ["Samosa","Bhootiya School","Cricket Match","Jadui Cycle","Chor Bazaar","Mela","Robot","Jungle","Barish","Exam","Golgappa","Diwali","Train","Kite"]
    topic = random.choice(topics)
    prompt = f"""Guddu aur Bholu ki funny Hindi kahani likho. Topic: {topic}. Sirf is format me do: TITLE: Guddu Bholu Ka {topic} Wala Kamaal STORY: 150 word ki funny kahani. 6 chhote scene me. Guddu hoshiyar, Bholu bhola. End me - subscribe karo."""
    to_try = ['gemini-3.8-flash']
    for key_no, api_key in enumerate(all_keys):
        try:
            print(f"--- Key {key_no+1} try kar raha hu ---")
            client = genai.Client(api_key=api_key)
            for model_name in to_try:
                try:
                    print(f"Trying: Key {key_no+1} + {model_name}")
                    res = client.models.generate_content(model=model_name, contents=prompt)
                    print(f"CHAL GAYA: Key {key_no+1} + {model_name}")
                    return res.text
                except Exception as e:
                    print(f"Fail {model_name}: {e}")
                    continue
        except Exception as e:
            print(f"Key {key_no+1} fail: {e}")
            continue
    raise Exception("Saari 6 key ki limit khatam")

try:
    full = get_new_story()
except Exception as e:
    print(f"AI fail: {e}")
    full = "TITLE: Guddu Bholu Ka Samosa Wala Kamaal\nSTORY: Ek din Guddu aur Bholu samosa khane gaye. Dukaan par bheed thi. Bholu bola bhaiya jaldi do. Guddu bola pehle paise de. Bholu ne jeb me haath dala, paise hi nahi the. Guddu hasne laga. Bholu bola aaj tu khila de, kal me khila dunga. Guddu ne samosa khilaya. Dono ne milkar samosa khaya aur haste hue ghar gaye. Aisi kahaniyo ke liye subscribe karo."

title = "Guddu Bholu Ki Kahani"
story = full
if "TITLE:" in full and "STORY:" in full:
    title = full.split("TITLE:")[1].split("STORY:")[0].strip().replace("*","").replace("#","")
    story = full.split("STORY:")[1].strip().replace("*","").replace("#","")
print(f"TITLE: {title}")

# 2. AUDIO
from gtts import gTTS
os.makedirs("output", exist_ok=True)
gTTS(text=story, lang='hi', slow=True).save("output/audio.mp3")
print("Audio ban gaya")

# 3. CARTOON + MOVEMENT - SHORTS SIZE
W, H = 1080, 1920
try:
    F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_big = ImageFont.truetype(F, 70)
    font_small = ImageFont.truetype(F, 48)
except:
    font_big = ImageFont.load_default()
    font_small = font_big

def draw_cartoon(d, cx, cy, color, name, frame, is_talking):
    bounce = int(math.sin(frame*0.5)*15) if is_talking else int(math.sin(frame*0.2)*5)
    y = cy + bounce
    d.ellipse([cx-110, y-100, cx+110, y+100], fill=color, outline=(0,0,0), width=6)
    if frame % 30 < 3:
        d.line([cx-50, y-20, cx-10, y-20], fill=(0,0,0), width=6)
        d.line([cx+10, y-20, cx+50, y-20], fill=(0,0,0), width=6)
    else:
        d.ellipse([cx-50, y-40, cx-10, y], fill=(255,255,255), outline=(0,0,0), width=3)
        d.ellipse([cx+10, y-40, cx+50, y], fill=(255,255,255), outline=(0,0,0), width=3)
        d.ellipse([cx-35, y-25, cx-20, y-10], fill=(0,0,0))
        d.ellipse([cx+20, y-25, cx+35, y-10], fill=(0,0,0))
    if is_talking:
        mouth_h = 20 + int(math.sin(frame*0.8)*20)
        d.ellipse([cx-30, y+30, cx+30, y+30+mouth_h], fill=(0,0,0))
    else:
        d.arc([cx-30, y+20, cx+30, y+60], 0, 180, fill=(0,0,0), width=5)
    d.text((cx-70, y+130), name, fill=(0,0,0), font=font_small)
    hand_y = y + 50 + int(math.sin(frame*0.6)*10)
    d.line([cx-110, y+20, cx-160, hand_y], fill=(0,0,0), width=8)
    d.line([cx+110, y+20, cx+160, hand_y], fill=(0,0,0), width=8)

sentences = [s.strip() for s in story.replace("\n"," ").split(".") if len(s.strip())>5]
scenes = []
for i in range(6):
    scenes.append(sentences[i] if i < len(sentences) else sentences[-1])

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
audio = AudioFileClip("output/audio.mp3")
total_dur = audio.duration
print(f"Audio Duration: {total_dur} sec, Video bhi utna hi banega")
scene_dur = total_dur / 6
clips = []
for si, scene_text in enumerate(scenes):
    for f in range(10):
        img = Image.new("RGB", (W, H), (135, 206, 235))
        d = ImageDraw.Draw(img)
        d.rectangle([0, 1400, W, H], fill=(34,139,34))
        d.rectangle([100, 900, 980, 1400], fill=(255, 210, 0))
        draw_cartoon(d, 300, 1150, (255,100,100), "GUDDU", f+si*10, si%2==0)
        draw_cartoon(d, 780, 1150, (100,200,255), "BHOLU", f+si*10, si%2!=0)
        lines = textwrap.wrap(scene_text, width=22)
        y = 150
        d.rectangle([50, 100, 1030, 100+len(lines)*90+40], fill=(255,255,255), outline=(0,0,0), width=4)
        for line in lines[:3]:
            d.text((80, y), line, fill=(0,0,0), font=font_big)
            y += 90
        d.text((80, 1650), f"{title} #Shorts", fill=(255,255,255), font=font_small, stroke_width=2, stroke_fill=(0,0,0))
        img.save(f"output/frame_{si}_{f}.jpg")
    scene_clips = [ImageClip(f"output/frame_{si}_{f}.jpg").set_duration(scene_dur/10) for f in range(10)]
    clips.append(concatenate_videoclips(scene_clips, method="compose"))

final = concatenate_videoclips(clips, method="compose").set_audio(audio).set_duration(total_dur)
final.write_videofile("output/final.mp4", fps=24, codec="libx264", audio_codec="aac")
print(f"VIDEO DONE - {total_dur} sec")

# 4. UPLOAD - SHORTS
print("Uploading...")
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
token_info = json.loads(os.environ["YOUTUBE_TOKEN"])
creds = Credentials.from_authorized_user_info(token_info)
youtube = build("youtube", "v3", credentials=creds)
req = youtube.videos().insert(part="snippet,status", body={"snippet": {"title": title+" #Shorts", "description": story[:4000]+"\n\n#Shorts #GudduBholu #HindiKahani", "tags": ["Guddu Bholu","Shorts","Hindi Kahani"], "categoryId": "24"}, "status": {"privacyStatus": "public", "madeForKids": True}}, media_body=MediaFileUpload("output/final.mp4"))
resp = req.execute()
print(f"UPLOAD HO GAYA! ID: {resp['id']}")
