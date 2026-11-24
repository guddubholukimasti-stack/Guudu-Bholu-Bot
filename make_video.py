import os
import requests
import subprocess
import sys
from pathlib import Path

HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")
CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

# 1 SCRIPT
script = ""
prompt = "Guddu aur Bholu ki funny Hindi story likho. 3 scene me. Dialog me. Guddu: Bholu: End me twist."

try:
    from groq import Groq
    client = Groq(api_key=GROQ_KEY)
    models = []
    models.append("llama-3.1-8b-instant")
    models.append("llama-3.3-70b-versatile")
    models.append("openai/gpt-oss-120b")
    for m in models:
        try:
            chat = client.chat.completions.create(
                model=m,
                messages=[{"role": "user", "content": prompt}]
            )
            script = chat.choices[0].message.content
            print("Model chala:", m)
            break
        except Exception as e:
            print("Model fail:", m)
            continue
except Exception as e:
    print("Groq error:", e)

if not script:
    script = "Guddu: Bholu aaj bada kaam hai.\n"
    script = script + "Bholu: Kaunsa kaam Guddu?\n"
    script = script + "Guddu: Aaj hum record todenge.\n"
    script = script + "Bholu: To chal jaldi, wait for end."

Path("script.txt").write_text(script, encoding="utf-8")
print("SCRIPT OK")

# 2 VOICE
lines = []
for l in script.splitlines():
    if ":" in l:
        lines.append(l.strip())

clean = ""
for l in lines:
    parts = l.split(":", 1)
    clean = clean + parts[1].strip() + " "
clean = clean[:900]

subprocess.run(
    [sys.executable, "-m", "edge_tts",
     "--voice", "hi-IN-MadhurNeural",
     "--file", "voice.mp3",
     "--text", clean],
    check=True
)
print("Voice ban gayi")

# 3 IMAGE FUNCTION
def make_image(prompt_text, out):
    try:
        headers = {}
        headers["Authorization"] = "Bearer " + str(HF_TOKEN)
        url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        data = {}
        data["inputs"] = prompt_text
        r = requests.post(url, headers=headers, json=data, timeout=120)
        if r.status_code == 200:
            open(out, "wb").write(r.content)
            print("Image ban gayi:", out)
            return True
    except Exception as e:
        print("Image fail:", e)
    return False

scene1 = "Cute cartoon Indian kids in house, 3D cartoon"
scene2 = "Cute cartoon Indian kids in village street, 3D cartoon"
scene3 = "Cute cartoon Indian kids laughing, funny twist, 3D cartoon"

low = script.lower()
if "jungle" in low:
    scene2 = "Cute cartoon Indian kids in jungle, 3D cartoon"
if "school" in low:
    scene1 = "Cute cartoon Indian kids in school, 3D cartoon"
if "dukaan" in low:
    scene2 = "Cute cartoon Indian kids in market, 3D cartoon"

ok1 = make_image(scene1, "img1.jpg")
ok2 = make_image(scene2, "img2.jpg")
ok3 = make_image(scene3, "img3.jpg")

# 4 MUSIC
has_music = False
try:
    music_url = "https://cdn.pixabay.com/download/audio/2022/03/10/audio_2c8c7b6b3e.mp3"
    r = requests.get(music_url, timeout=30)
    open("music.mp3", "wb").write(r.content)
    print("Music aa gayi")
    has_music = True
except Exception as e:
    print("Music fail:", e)

# 5 VIDEO
if ok1 and ok2 and ok3:
    f = open("list.txt", "w")
    f.write("file 'img1.jpg'\n")
    f.write("duration 10\n")
    f.write("file 'img2.jpg'\n")
    f.write("duration 10\n")
    f.write("file 'img3.jpg'\n")
    f.write("duration 10\n")
    f.write("file 'img3.jpg'\n")
    f.close()
    cmd = []
    cmd.append("ffmpeg")
    cmd.append("-y")
    cmd.append("-f")
    cmd.append("concat")
    cmd.append("-safe")
    cmd.append("0")
    cmd.append("-i")
    cmd.append("list.txt")
    cmd.append("-i")
    cmd.append("voice.mp3")
    cmd.append("-c:v")
    cmd.append("libx264")
    cmd.append("-pix_fmt")
    cmd.append("yuv420p")
    cmd.append("-c:a")
    cmd.append("aac")
    cmd.append("-shortest")
    cmd.append("temp.mp4")
    subprocess.run(cmd, check=True)
else:
    cmd2 = []
    cmd2.append("ffmpeg")
    cmd2.append("-y")
    cmd2.append("-loop")
    cmd2.append("1")
    cmd2.append("-i")
    cmd2.append("img1.jpg")
    cmd2.append("-i")
    cmd2.append("voice.mp3")
    cmd2.append("-c:v")
    cmd2.append("libx264")
    cmd2.append("-t")
    cmd2.append("30")
    cmd2.append("-pix_fmt")
    cmd2.append("yuv420p")
    cmd2.append("-c:a")
    cmd2.append("aac")
    cmd2.append("-shortest")
    cmd2.append("temp.mp4")
    subprocess.run(cmd2, check=True)

# 6 MUSIC MIX
if has_music:
    cmd3 = []
    cmd3.append("ffmpeg")
    cmd3.append("-y")
    cmd3.append("-i")
    cmd3.append("temp.mp4")
    cmd3.append("-i")
    cmd3.append("music.mp3")
    cmd3.append("-filter_complex")
    cmd3.append("[1:a]volume=0.15[music];[0:a][music]amix=inputs=2:duration=first[a]")
    cmd3.append("-map")
    cmd3.append("0:v")
    cmd3.append("-map")
    cmd3.append("[a]")
    cmd3.append("-c:v")
    cmd3.append("copy")
    cmd3.append("-c:a")
    cmd3.append("aac")
    cmd3.append("-shortest")
    cmd3.append("final_video.mp4")
    subprocess.run(cmd3, check=True)
else:
    subprocess.run(["cp", "temp.mp4", "final_video.mp4"], check=True)

print("Final video ban gaya")

# 7 UPLOAD
try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.oauth2.credentials import Credentials
    creds = Credentials(
        None,
        refresh_token=REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    yt = build("youtube", "v3", credentials=creds)
    title = "Guddu Bholu Ki Funny Story | Wait For End #shorts"
    desc = script[:1000] + "\n\n#guddu #bholu #funny #shorts"
    snippet = {}
    snippet["title"] = title
    snippet["description"] = desc
    snippet["tags"] = ["guddu", "bholu", "funny", "shorts"]
    snippet["categoryId"] = "23"
    status = {}
    status["privacyStatus"] = "public"
    status["selfDeclaredMadeForKids"] = True
    body_data = {}
    body_data["snippet"] = snippet
    body_data["status"] = status
    req = yt.videos().insert(
        part="snippet,status",
        body=body_data,
        media_body=MediaFileUpload("final_video.mp4")
    )
    res = req.execute()
    print("UPLOAD HO GAYA:", res["id"])
except Exception as e:
    print("Upload fail:", e)
