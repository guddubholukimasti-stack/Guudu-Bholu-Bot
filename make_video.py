import os
import requests
import subprocess
import sys
import asyncio
import shutil
from pathlib import Path

print("=== SELF HEALING START ===")

HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")
CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

# AUTO FIX 1 - ffmpeg nahi hai to install kar le
if shutil.which("ffmpeg") is None:
    print("ffmpeg nahi mila, install kar raha hu...")
    try:
        subprocess.run(["sudo", "apt-get", "update"], check=False)
        subprocess.run(["sudo", "apt-get", "install", "-y", "ffmpeg"], check=False)
    except Exception as e:
        print("ffmpeg install fail:", e)
else:
    print("ffmpeg mil gaya")

# 1 SCRIPT - 3 model try karega
script = ""
prompt = "Guddu aur Bholu ki funny Hindi story likho. Sirf dialog likho. Jaise Guddu: ... Bholu: ... Koi bracket, koi star mat likho. 8 dialog se zyada mat likho."

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
            print("Model fail, dusra try:", m)
            continue
except Exception as e:
    print("Groq fail:", e)

if not script:
    print("Sab model fail, backup story le raha hu")
    script = "Guddu: Bholu aaj bada kaam hai.\nBholu: Kaunsa kaam Guddu?\nGuddu: Aaj hum record todenge.\nBholu: To chal jaldi, wait for end."

Path("script.txt").write_text(script, encoding="utf-8")
print("SCRIPT OK")

# 2 VOICE - 3 voice try karega, wahi teri wali pehle
lines = []
for l in script.splitlines():
    if ":" in l:
        lines.append(l.strip())
lines = lines[:8]

clean = ""
for l in lines:
    parts = l.split(":", 1)
    t = parts[1].strip()
    for c in ["**", "*", "(", ")", "[", "]", "#"]:
        t = t.replace(c, "")
    clean = clean + t + " "
clean = clean[:600]
print("Voice text:", clean)

async def try_voice(voice_name):
    import edge_tts
    com = edge_tts.Communicate(clean, voice_name)
    await com.save("voice.mp3")

voices = ["hi-IN-MadhurNeural", "hi-IN-SwaraNeural", "hi-IN-MadhurNeural"]
voice_ok = False
for v in voices:
    try:
        asyncio.run(try_voice(v))
        print("Voice ban gayi:", v)
        voice_ok = True
        break
    except Exception as e:
        print("Voice fail, dusri try:", v)

if not voice_ok:
    print("Voice nahi bani, silent audio bana raha hu")
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "10", "voice.mp3"], check=False)

# 3 IMAGE - 2 model try karega
def make_image(prompt_text, out):
    urls = [
        "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0",
        "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    ]
    for url in urls:
        try:
            headers = {"Authorization": "Bearer " + str(HF_TOKEN)}
            r = requests.post(url, headers=headers, json={"inputs": prompt_text}, timeout=120)
            if r.status_code == 200 and len(r.content) > 5000:
                open(out, "wb").write(r.content)
                print("Image ban gayi:", out)
                return True
        except Exception as e:
            print("Image fail, dusra try")
            continue
    return False

scene1 = "Cute cartoon Indian kids in house, 3D cartoon"
low = script.lower()
if "jungle" in low:
    scene1 = "Cute cartoon Indian kids in jungle, 3D cartoon"
if "school" in low:
    scene1 = "Cute cartoon Indian kids in school, 3D cartoon"
if "dukaan" in low:
    scene1 = "Cute cartoon Indian kids in market, 3D cartoon"

ok1 = make_image(scene1, "img1.jpg")
if not ok1:
    print("Image nahi bani, blank image bana raha hu")
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=0x1a1a2e:s=720x1280", "-frames:v", "1", "img1.jpg"], check=False)

# 4 MUSIC - nahi mili to bina music ke
has_music = False
try:
    r = requests.get("https://cdn.pixabay.com/download/audio/2022/03/10/audio_2c8c7b6b3e.mp3", timeout=30)
    if len(r.content) > 1000:
        open("music.mp3", "wb").write(r.content)
        has_music = True
        print("Music aa gayi")
except Exception as e:
    print("Music fail, bina music ke chalega")

# 5 VIDEO - kabhi rukega nahi
try:
    subprocess.run(["ffmpeg", "-y", "-loop", "1", "-i", "img1.jpg", "-i", "voice.mp3", "-c:v", "libx264", "-t", "30", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "temp.mp4"], check=True)
    print("Video ban gaya")
except Exception as e:
    print("Video fail, dobara try:", e)
    subprocess.run(["ffmpeg", "-y", "-loop", "1", "-i", "img1.jpg", "-i", "voice.mp3", "-c:v", "mpeg4", "-t", "30", "-c:a", "aac", "-shortest", "temp.mp4"], check=False)

# 6 MUSIC MIX
try:
    if has_music and Path("temp.mp4").exists():
        subprocess.run(["ffmpeg", "-y", "-i", "temp.mp4", "-i", "music.mp3", "-filter_complex", "[1:a]volume=0.15[music];[0:a][music]amix=inputs=2:duration=first[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-shortest", "final_video.mp4"], check=True)
    else:
        shutil.copy("temp.mp4", "final_video.mp4")
    print("Final video ban gaya")
except Exception as e:
    print("Mix fail, temp ko hi final bana raha hu")
    if Path("temp.mp4").exists():
        shutil.copy("temp.mp4", "final_video.mp4")

# 7 UPLOAD - fail hua to video save rahega
try:
    from googleapiclient.discovery import build
    from googleapiclient.http import Media
