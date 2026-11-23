import os, requests, random, json, subprocess
from datetime import date
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# ============ 1. GEMINI SE NAYI KAHANI ============
def get_story():
    api_key = os.getenv("GEMINI_API_KEY")
    topics = ["samosa","cricket","bhoot","school","cycle","barish","mela","mobile","exam","chai","patang","bakri","train","shaadi","paisa","jadu","chor","dost","baigan","doctor"]
    topic = random.choice(topics)
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        prompt = f"Guddu, Bholu aur Chintu ki ek bahut funny, 40-50 words ki Hindi Hinglish kahani likho. Topic: {topic}. Kahani bilkul nayi ho, ending me funny twist ho. Sirf kahani likho, title mat do."
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
        story = r.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        title = f"Guddu Bholu Ka {topic.capitalize()} Wala Kaand! 😂 #shorts #funny"
        return title, story
    except Exception as e:
        print("AI fail:", e)
        return "Guddu Bholu Samosa Mission 😂 #shorts", "Guddu ne Bholu se kaha aaj samosa free hai! Bholu daud ke gaya, waha Chintu pehle se 10 samose kha raha tha! Bholu bola, bhai ek to de de!"

title, story = get_story()
print("TITLE:", title)
print("STORY:", story)

# ============ 2. VOICE BANAO ============
tts = gTTS(text=story, lang='hi')
tts.save("voice.mp3")

# ============ 3. PHOTO BANAO (Background) ============
W, H = 1080, 1920
img = Image.new("RGB", (W, H), (255, 180, 0))
draw = ImageDraw.Draw(img)
# Bada text upar
try:
    font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 45)
except:
    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()

draw.text((80, 200), "GUDDU BHOLU", fill=(0,0,0), font=font_big)
draw.text((80, 300), "CHINTU", fill=(255,255,255), font=font_big)

# Kahani ka text beech me wrap karke
words = story.split()
lines = []
line = ""
for w in words:
    if len(line + " " + w) < 30:
        line += " " + w
    else:
        lines.append(line.strip())
        line = w
lines.append(line.strip())

y = 700
for l in lines:
    draw.text((80, y), l, fill=(0,0,0), font=font_small)
    y += 65

img.save("bg.jpg")
print("Photo ban gayi")

# ============ 4. VIDEO BANAO ============
# voice.mp3 + bg.jpg = final.mp4 (9:16 Shorts)
cmd = [
    "ffmpeg", "-y",
    "-loop", "1", "-i", "bg.jpg",
    "-i", "voice.mp3",
    "-c:v", "libx264", "-tune", "stillimage",
    "-c:a", "aac", "-b:a", "192k",
    "-pix_fmt", "yuv420p", "-shortest",
    "final.mp4"
]
subprocess.run(cmd, check=True)
print("Video ban gaya")

# ============ 5. YOUTUBE PE DALO ============
# Token GitHub Secret YOUTUBE_TOKEN se aayega
token_json = os.getenv("YOUTUBE_TOKEN")
if token_json:
    creds = Credentials.from_authorized_user_info(json.loads(token_json))
    youtube = build("youtube", "v3", credentials=creds)
    body = {
        "snippet": {"title": title, "description": story + "\n\n#shorts #guddubholu #funny #comedy", "categoryId": "23"},
        "status": {"privacyStatus": "public", "madeForKids": False}
    }
    media = MediaFileUpload("final.mp4", chunksize=-1, resumable=True, mimetype="video/mp4")
    req = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = req.execute()
    print("UPLOAD HO GAYA! Video ID:", resp["id"])
else:
    print("YOUTUBE_TOKEN nahi mila, upload skip - video final.mp4 me ban gaya hai")
