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
    font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
    font_small = ImageFont.truetype("/usr/share/fonts/tr
