import os, random, textwrap, datetime
from PIL import Image, ImageDraw, ImageFont

# 1. GEMINI SE HAR BAAR NAYI KAHANI
def get_new_story():
    import google.generativeai as genai
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("AI fail: KEY NAHI MILI")
        raise Exception("no key")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    topics = ["Samosa", "Bhootiya School", "Cricket Match", "Jadui Cycle", "Chor Bazaar", "Mela", "Robot", "Jungle", "Barish", "Exam", "Golgappa", "Diwali", "Train", "Kite"]
    topic = random.choice(topics)
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    prompt = f"""Guddu aur Bholu ki ekdam nayi funny Hindi kahani likho. Topic: {topic}. Date: {date}.
    Sirf is format me do:
    TITLE: Guddu Bholu Ka {topic} Wala Kamaal
    STORY: 600 word ki funny kahani. Guddu hoshiyar hai, Bholu bhola hai. End me likhna - Aisi hi kahaniyo ke liye channel ko subscribe karo."""
    res = model.generate_content(prompt)
    print("GEMINI SE NAYI KAHANI AA GAYI")
    return res.text

try:
    full = get_new_story()
except Exception as e:
    print(f"AI fail: {e}")
    full = "TITLE: Guddu Bholu Ka Golgappa Wala Kamaal\nSTORY: Ek din Guddu aur Bholu golgappa khane gaye. Bholu ne 100 golgappe kha liye aur pet ful gaya. Guddu ne usko paani pilaya aur dono hasne lage. Aisi hi kahaniyo ke liye channel ko subscribe karo"

title = "Guddu Bholu Ki Kahani"
story = full
if "TITLE:" in full and "STORY:" in full:
    title = full.split("TITLE:")[1].split("STORY:")[0].strip().replace("*","").replace("#","")
    story = full.split("STORY:")[1].strip().replace("*","").replace("#","")

print(f"TITLE: {title}")
print(f"STORY: {story[:200]}")

# 2. AUDIO
from gtts import gTTS
os.makedirs("output", exist_ok=True)
gTTS(text=story, lang='hi', slow=False).save("output/audio.mp3")
print("Audio ban gaya")

# 3. THUMBNAIL - BADA TEXT
img = Image.new("RGB", (1280, 720), (255, 210, 0))
d = ImageDraw.Draw(img)
try:
    font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 95)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55)
except:
    font_big = ImageFont.load_default()
    font_small = font_big

lines = textwrap.wrap(title, width=16)
y = 130
for line in lines[:2]:
    d.text((50, y), line, fill=(255,0,0), font=font_big, stroke_width=5, stroke_fill=(0,0,0))
    y += 120
d.text((50, 520), "GUDDU BHOLU", fill=(0,0,0), font=font_small)
img.save("output/thumbnail.jpg")
print("Thumbnail ban gaya")

# 4. VIDEO
from moviepy.editor import ImageClip, AudioFileClip
audio = AudioFileClip("output/audio.mp3")
clip = ImageClip("output/thumbnail.jpg").set_duration(audio.duration).set_audio(audio)
clip.write_videofile("output/final.mp4", fps=24, codec="libx264", audio_codec="aac")
print("VIDEO DONE")
# 5. UPLOAD TO YOUTUBE
print("Uploading to YouTube...")
import json, pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

token_info = json.loads(os.environ["YOUTUBE_TOKEN"])
creds = Credentials.from_authorized_user_info(token_info)
youtube = build("youtube", "v3", credentials=creds)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {"title": title, "description": story[:4000], "tags": ["Guddu Bholu", "Hindi Kahani"], "categoryId": "27"},
        "status": {"privacyStatus": "public", "madeForKids": True}
    },
    media_body=MediaFileUpload("output/final.mp4")
)
resp = request.execute()
print(f"UPLOAD HO GAYA! Video ID: {resp['id']}")
