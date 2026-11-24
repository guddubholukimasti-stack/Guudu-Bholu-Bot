import os, requests, subprocess, sys, re
from pathlib import Path

HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")
CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

# 1. SCRIPT
script = ""
prompt = "Guddu aur Bholu ki funny Hindi story likho, 60 second ki. 3 scene me likho. Scene 1: Ghar, Scene 2: Bahar, Scene 3: Twist. Dialog format me Guddu: ... Bholu: ... End me twist rakho."

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
            print("Model fail:", m)
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
subprocess.run([sys.executable, "-m", "edge_tts", "--voice", "hi-IN-MadhurNeural", "--file", "voice.mp3", "--text", clean], check=True)
print("Voice ban gayi")

# 3. SCENE KE HISAB SE 3 BACKGROUND IMAGE
def make_image(prompt_text, out):
    try:
        headers = {"Authorization": "Bearer " + str(HF_TOKEN)}
        r = requests.post("https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0", headers=headers, json={"inputs": prompt_text}, timeout=120)
        if r.status_code == 200:
            open(out, "wb").write(r.content)
            print("Image ban gayi:", out)
            return True
    except Exception as e:
        print("Image fail:", e)
    return False

# Script se scene nikal ke prompt banao
scene1 = "Cute cartoon Indian kids in a house, 3D cartoon style, bright colors"
scene2 = "Cute cartoon Indian kids outside in village street, 3D cartoon style, bright colors"
scene3 = "Cute cartoon Indian kids surprised and laughing, funny twist, 3D cartoon style"

# Agar script me jungle / school / dukaan word hai to us hisab se badlo
low = script.lower()
if "jungle" in low or "jangal" in low:
    scene2 = "Cute cartoon Indian kids in jungle, funny, 3D cartoon style"
if "school" in low:
    scene1 = "Cute cartoon Indian kids in school classroom, 3D cartoon style"
if "dukaan" in low or "bazaar" in low:
    scene2 = "Cute cartoon Indian kids in market shop, 3D cartoon style"

ok1 = make_image(scene1, "img1.jpg")
ok2 = make_image(scene2, "img2.jpg")
ok3 = make_image(scene3, "img3.jpg")

# 4. BACKGROUND MUSIC DOWNLOAD - Free funny music
try:
    music_url = "https://cdn.pixabay.com/download/audio/2022/03/10/audio_2c8c7b6b3e.mp3"
    r = requests.get(music_url, timeout=30)
    open("music.mp3", "wb").write(r.content)
    print("Music aa gayi")
    has_music = True
except Exception as e:
    print("Music fail, bina music ke banega:", e)
    has_music = False

# 5. VIDEO BANANA - 3 Image badlenge
if ok1 and ok2 and ok3:
    # 3 image ko 10-10 sec ke liye jodo
    open("list.txt", "w").write("file 'img1.jpg'\nduration 10\nfile 'img2.jpg'\nduration 10\nfile 'img3.jpg'\nduration 10\nfile 'img3.jpg'\n")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "list.txt", "-i", "voice.mp3", "-c:v", "libx264", "-
