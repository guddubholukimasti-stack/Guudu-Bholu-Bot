import os, requests, subprocess, sys
from pathlib import Path

HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")
CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

print("Keys check:", bool(HF_TOKEN), bool(GROQ_KEY))

# 1. SCRIPT
script = ""
prompt = "Guddu aur Bholu ki funny Hindi story likho, 60 second ki. Guddu hoshiyar hai, Bholu gadha hai. Dialog format me likho Guddu: ... Bholu: ... End me twist rakho. Sirf dialog likho."

try:
    from groq import Groq
    client = Groq(api_key=GROQ_KEY)
    models = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "openai/gpt-oss-120b"]
    for m in models:
        try:
            chat = client.chat.completions.create(model=m, messages=[{"role": "user", "content": prompt}])
            script = chat.choices[0].message.content
            print("Model chala:", m)
            break
        except Exception as e:
            print("Model fail:", m, e)
            continue
except Exception as e:
    print("Groq error:", e)

if not script:
    script = "Guddu: Bholu aaj bada kaam hai bhai.\nBholu: Kaunsa kaam Guddu?\nGuddu: Aaj hum record todenge.\nBholu: To chal jaldi, wait for end."

Path("script.txt").write_text(script, encoding="utf-8")
print("SCRIPT OK")

# 2. VOICE
lines = [l.strip() for l in script.splitlines() if ":" in l]
clean = " ".join([l.split(":", 1)[1].strip() for l in lines]) if lines else script
clean = clean[:900]
print("VOICE TEXT:", clean[:80])

subprocess.run([sys.executable, "-m", "edge_tts", "--voice", "hi-IN-MadhurNeural", "--file", "voice.mp3", "--text", clean], check=True)
print("Voice ban gayi")

# 3. IMAGE
has_image = False
try:
    headers = {"Authorization": "Bearer " + str(HF_TOKEN)}
    img_prompt = "Cute cartoon Indian kids, two funny boys, colorful village, 3D cartoon style"
    r = requests.post("https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0", headers=headers, json={"inputs": img_prompt}, timeout=120)
    if r.status_code == 200:
        open("image.jpg", "wb").write(r.content)
        has_image = True
        print("Image ban gayi")
    else:
        print("HF fail:", r.status_code)
except Exception as e:
    print("HF error:", e)

# 4. VIDEO
if has_image:
    cmd = ["ffmpeg", "-y", "-loop", "1", "-i", "image.jpg", "-i", "voice.mp3", "-c:v", "libx264", "-t", "30", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "final_video.mp4"]
else:
    cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=0x1a1a2e:s=720x1280:d=30", "-i", "voice.mp3", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "final_video.mp4"]

subprocess.run(cmd, check=True)
print("Video ban gaya")

# 5. UPLOAD
try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.oauth2.credentials import Credentials

    creds = Credentials(None, refresh_token=REFRESH_TOKEN, token_uri="https://oauth2.googleapis.com/token", client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    yt = build("youtube", "v3", credentials=creds)
    title = "Guddu Bholu Ki Funny Story | Wait For End #shorts"
    desc = script[:1000] + "\n\n#guddu #bholu #funny #shorts"
    body_data = {}
    body_data["snippet"] = {"title": title, "description": desc, "tags": ["guddu", "bholu", "funny", "shorts"], "categoryId": "23"}
    body_data["status"] = {"privacyStatus": "public", "selfDeclaredMadeForKids": True}
    req = yt.videos().insert(part="snippet,status", body=body_data, media_body=MediaFileUpload("final_video.mp4"))
    res = req.execute()
    print("UPLOAD HO GAYA:", res["id"])
except Exception as e:
    print("Upload fail:", e)
