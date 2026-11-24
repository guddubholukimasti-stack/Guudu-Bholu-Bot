# FINAL SYSTEM - 30 DAYS - Roz 9 Baje Auto Video
# Background ke hisaab se Script + Hilta hua Cartoon + Desi Voice

import os
import datetime
import requests
import asyncio
import edge_tts
from groq import Groq

# --- 1. KEYS ---
HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")

# --- 2. 30 DAYS PLAN - Tarikh se chalega ---
PLANS = [
    {"bg": "Labour Chowk, yellow board, dust, Indian street, thela", "topic": "Ghar todne ka kaam, labour chahiye", "top_text": "Ghar todne ka kaam"},
    {"bg": "Chauraha, chai ki dukaan, bikes, crowd, Indian street", "topic": "Chai pe joke, kadak chai", "top_text": "Chai Pe Charcha"},
    {"bg": "Gali, house breaking, cement, sand, workers", "topic": "Deewar todni hai, makan todna hai", "top_text": "Deewar Todni Hai"},
    {"bg": "Construction site, big building, crane, workers", "topic": "Crane wala, building ka kaam", "top_text": "Building Todni Hai"},
    {"bg": "Sabzi Mandi, thela, crowd, vegetables", "topic": "Sabzi mandi me bargaining, biwi pe punch", "top_text": "Sabzi Mandi Me Hungama"},
    {"bg": "Bus Stand, auto, people waiting, Indian bus stand", "topic": "Bus ka wait, auto wala", "top_text": "Bus Ka Wait"},
    {"bg": "House gate, broken wall, home exterior", "topic": "Ghar ke bahar ka kaam, gate tuta hai", "top_text": "Ghar Ka Kaam"},
    {"bg": "Pan ki dukaan, paan, gutkha, chauraha", "topic": "Paan wala aur biwi ka gussa", "top_text": "Paan Wala Bhaiya"},
    {"bg": "Kirana store, ration ki dukaan, bheed", "topic": "Udhar pe samaan, biwi ka list", "top_text": "Kirana Store Ka Udhar"},
    {"bg": "Nai ki dukaan, salon, baal kat rahe hai", "topic": "Baal katwane gaya, biwi ne pehchana nahi", "top_text": "Salon Me Hungama"},
    {"bg": "Hospital ke bahar, doctor, line", "topic": "Doctor ko dikhane gaya, biwi ki daant", "top_text": "Doctor Ke Paas"},
    {"bg": "School ke bahar, bachche, cycle, parents", "topic": "Bachche ko school chhodne gaya", "top_text": "School Ka Drama"},
    {"bg": "Railway station, train, kulfi wala, bheed", "topic": "Train late hai, biwi gussa", "top_text": "Train Late Hai"},
    {"bg": "Petrol pump, bike pe petrol bharwa raha", "topic": "Petrol mehenga, biwi ka taana", "top_text": "Petrol Mehenga Hai"},
    {"bg": "Bank ke bahar, ATM line, log khade", "topic": "Paisa nikalne gaya, ATM kharab", "top_text": "ATM Kharab Hai"},
    {"bg": "Mandir ke bahar, prasad, bheed, pujari", "topic": "Mandir gaya, biwi ne mannat mangi", "top_text": "Mandir Me Mannat"},
    {"bg": "Bazaar, kapde ki dukaan, saree, bheed", "topic": "Biwi ko saree dilane gaya, jeb khali", "top_text": "Saree Ki Dukaan"},
    {"bg": "Dhaba, highway, truck, khana kha raha", "topic": "Dhabe pe khana, biwi ka phone", "top_text": "Dhabe Pe Khana"},
    {"bg": "Park, bench, bachche khel rahe, morning walk", "topic": "Park me walk, biwi ki daant", "top_text": "Park Me Walk"},
    {"bg": "Police station ke bahar, police, bike", "topic": "Challan kat gaya, biwi ka gussa", "top_text": "Challan Kat Gaya"},
    {"bg": "Mobile shop, phone repair, bheed", "topic": "Phone tut gaya, biwi ka gussa", "top_text": "Phone Tut Gaya"},
    {"bg": "Cycle ki dukaan, puncture wala", "topic": "Cycle puncture, biwi ka taana", "top_text": "Cycle Puncture Ho Gaya"},
    {"bg": "Halwai ki dukaan, jalebi, samosa, bheed", "topic": "Jalebi kha raha tha, biwi ne dekh liya", "top_text": "Jalebi Ka Chakkar"},
    {"bg": "Tailor ki dukaan, silai machine, kapde", "topic": "Kapde silwane gaya, biwi ka napa", "top_text": "Tailor Ki Dukaan"},
    {"bg": "Barber shop ke bahar, darhi bana raha", "topic": "Dadhi banwayi, biwi ne pehchana nahi", "top_text": "Dadhi Banwayi"},
    {"bg": "Gym ke bahar, dumbbell, ladke exercise", "topic": "Gym gaya, body nahi bani, biwi has rahi", "top_text": "Gym Ka Hero"},
    {"bg": "Chai thela, raat ka scene, light, bheed", "topic": "Raat ko chai peene gaya, biwi ka phone", "top_text": "Raat Ki Chai"},
    {"bg": "Rickshaw stand, rickshaw wala, sawari", "topic": "Rickshaw wala zyada paise mang raha", "top_text": "Rickshaw Wala"},
    {"bg": "Nadi kinare, pul, log baithe, shaam", "topic": "Nadi pe ghumne gaya, biwi ka call", "top_text": "Nadi Kinare"},
    {"bg": "Shadi ka tent, dulhan, DJ, lights, bheed", "topic": "Shadi me gaya, biwi ne dance karwaya", "top_text": "Shadi Me Dance"},
]

aaj_tarikh = datetime.datetime.now().day
index = (aaj_tarikh - 1) % 30
plan = PLANS[index]
print(f"Aaj {aaj_tarikh} tarikh hai | Plan: {plan['top_text']} | BG: {plan['bg']}")

# --- 3. GROQ SE SCRIPT - Background ke hisaab se ---
client = Groq(api_key=GROQ_KEY)
prompt = f"""
Background hai: {plan['bg']}
Topic hai: {plan['topic']}

Is background pe 30 second ka funny Hindi dialogue bana.
2 characters: Guddu (ladka, desi) aur Bholu (ladki, nakhre wali)
Pehle 2 sec me hook ho.
Beech me confusion ho.
Last me bada punchline ho, biwi pe joke ho.
Sirf dialogue de, aise:
Guddu: ...
Bholu: ...
"""
chat = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}]
)
script = chat.choices[0].message.content
print("SCRIPT:", script)
full_text = script.replace("Guddu:", "").replace("Bholu:", "").replace("\n", " ")

# --- 4. EDGE-TTS VOICE ---
async def make_voice():
    c = edge_tts.Communicate(full_text, "hi-IN-MadhurNeural", rate="+10%")
    await c.save("voice.mp3")
asyncio.run(make_voice())
print("Voice ban gayi")

# --- 5. HF WAN VIDEO ---
headers = {"Authorization": f"Bearer {HF_TOKEN}"}
try:
    r = requests.post(
        "https://api-inference.huggingface.co/models/Wan-AI/Wan2.1-T2V-1.3B",
        headers=headers,
        json={"inputs": f"Funny Indian 3D cartoon, Guddu orange hair big head, Bholu girl black hair glasses pink suit, background {plan['bg']}, talking, moving mouth, eyes blinking, funny expressions"},
        timeout=300
    )
    if r.status_code == 200 and len(r.content) > 10000:
        open("raw_video.mp4", "wb").write(r.content)
        print("HF Video OK")
    else:
        print(f"HF Fail {r.status_code}")
        raise Exception("HF fail")
except Exception as e:
    print(f"Backup mode: {e}")
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (720, 1280), color=(255, 220, 100))
    d = ImageDraw.Draw(img)
    d.text((50, 500), plan['top_text'], fill=(0, 0, 0))
    img.save("backup.jpg")
    from moviepy.editor import ImageClip
    ImageClip("backup.jpg").set_duration(30).write_videofile("raw_video.mp4", fps=24)

# --- 6. FINAL JODNA ---
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

video = VideoFileClip("raw_video.mp4")
if video.duration > 30:
    video = video.subclip(0, 30)
audio = AudioFileClip("voice.mp3")
video = video.set_audio(audio)

try:
    top = TextClip(plan['top_text'], fontsize=60, color='yellow', font='DejaVu-Sans-Bold', stroke_color='black', stroke_width=2).set_position(('center', 30)).set_duration(video.duration)
    bottom = TextClip("wait for end", fontsize=50, color='white', bg_color='black', font='DejaVu-Sans-Bold').set_position(('center', video.h - 120)).set_duration(video.duration)
    final = CompositeVideoClip([video, top, bottom])
except Exception as e:
    print(f"Text fail, bina text ke: {e}")
    final = video

final.write_videofile("final_video.mp4", codec="libx264", audio_codec="aac", fps=24)
print("FINAL READY:", plan['top_text'])

# --- 7. YOUTUBE UPLOAD ---
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def upload_youtube():
    creds = Credentials(None, refresh_token=os.getenv("YOUTUBE_REFRESH_TOKEN"),
        client_id=os.getenv("YOUTUBE_CLIENT_ID"),
        client_secret=os.getenv("YOUTUBE_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token")
    yt = build("youtube", "v3", credentials=creds)
    req = yt.videos().insert(part="snippet,status", body={
        "snippet": {"title": f"{plan['top_text']} 😂 | wait for end", "description": f"{plan['topic']} #shorts #funny #comedy", "categoryId": "23", "tags": ["funny", "comedy", "shorts"]},
        "status": {"privacyStatus": "public"}
    }, media_body=MediaFileUpload("final_video.mp4"))
    print(req.execute())

upload_youtube()
