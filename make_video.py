import os, random, datetime
import textwrap, math, json, subprocess
from PIL import Image, ImageDraw, ImageFont

# ============ DATE - HAR ROZ ALAG ============
today = datetime.datetime.now()
day_num = today.timetuple().tm_yday
random.seed(day_num)
print("Aaj:", today.strftime("%d %b"), "Day:", day_num)

# ============ 1. KAHANI - 10 KAHANI, ROZ ALAG, LAMBI, REPEAT NAHI ============
def get_new_story():
    stories = [
        ("Guddu ne Bholu ka samosa kha liya", "samosa", "Ek din Guddu aur Bholu mela ghoomne gaye. Mela me bahut bheed thi aur samose ki khushboo aa rahi thi. Bholu ne apne paise se ek garam samosa liya. Bholu bola bhai ye samosa to bahut tasty lag raha hai. Guddu ne bola mujhe bhi thoda taste karne de. Bholu ne bola nahi ye mera samosa hai. Guddu ne chupke se samosa utha liya aur kha gaya. Bholu bola are mera samosa kahan gaya. Guddu bola maine to bas dekha tha, samosa to ud gaya. Bholu ko bahut gussa aa gaya. Guddu ko apni galti samajh aa gayi. Guddu bola sorry bhai, chal me tujhe do samose khilata hu. Dono ne milke samosa khaya aur bahut hasse. Aakhir me dono haste hue ghar gaye."),
        ("Bholu ko girlfriend ne paise diye", "paise", "Ek din Bholu school se ghar aa raha tha. Raste me uski girlfriend mil gayi. Girlfriend ne Bholu ko paise diye. Bholu bahut khush ho gaya aur uchalne laga. Guddu bola bhai itna khush kyun hai. Bholu bola aaj to party hogi. Guddu bola party me kya khayenge. Bholu bola pehle samosa khayenge phir jalebi khayenge. Dono dukaan pe gaye aur samosa khaya. Dukaan wale ne bola paise kaun dega. Bholu bola me dunga mere paas paise hai. Guddu hasne laga aur bola tu to ameer ho gaya. Dono ne milke party ki. Aakhir me dono haste hue ghar gaye."),
        ("Guddu ne Bholu ko ullu banaya", "ullu", "Ek din Guddu ne Bholu ko ullu banaya. Bola dekh peeche bandar hai. Bholu peeche dekhne laga. Guddu hasne laga. Bholu bola tu to bada chalak hai. Guddu bola chal ab mela chalte hai. Dono mela gaye aur jhoola jhoole. Mela me dono ne golgappe khaye. Bholu ne bola aaj to maza aa gaya. Dono ne bahut masti ki. Aakhir me dono haste hue ghar gaye."),
        ("Bholu ne Guddu ki cycle tod di", "cycle", "Ek din Bholu ne Guddu ki cycle tod di. Guddu bola ab me school kaise jaunga. Bholu bola tension mat le me theek kar dunga. Dono ne milke cycle theek ki. Phir dono cycle pe ghoomne gaye. Raste me barish aa gayi aur dono bheeg gaye. Bholu bola bhai barish me maza aa raha hai. Guddu bola chal jaldi ghar chalte hai. Dono haste hue ghar gaye aur mummy ko kahani sunayi."),
        ("Guddu Bholu ka cricket match", "cricket", "Ek din Guddu aur Bholu cricket khelne gaye. Guddu ne pehli ball pe chhakka mara. Bholu bola bhai tu to bada player hai. Bholu ne bhi chhakka mara. Dono ki team jeet gayi. Sab ne taali bajayi. Guddu bola aaj to hum champion hai. Bholu bola chal samosa khate hai. Dono ne milke samosa khaya. Dono bahut khush hue aur ghar gaye."),
        ("Guddu Bholu train me fas gaye", "train", "Ek din Guddu aur Bholu train me ghoomne gaye. Train bahut tez chal rahi thi. Bholu bola mujhe dar lag raha hai. Guddu bola dar mat me hu na. Train ruk gayi aur dono utar gaye. Dono ne station pe samosa khaya. Station pe dono ne bahut masti ki. Log dono ko dekh ke hasne lage. Dono haste hue ghar gaye."),
        ("Guddu Bholu ka exam wala din", "exam", "Ek din Guddu aur Bholu ka exam tha. Bholu ne padhai nahi ki thi. Guddu bola tension mat le me sikha dunga. Guddu ne Bholu ko sab sikha diya. Dono ka exam accha gaya. Teacher ne dono ko shabaashi di. Bholu bola bhai tu to best hai. Guddu bola chal ab mela chalte hai. Dono khush ho ke ghar gaye."),
        ("Bholu ne Guddu ka phone tod diya", "phone", "Ek din Bholu ne Guddu ka phone tod diya. Guddu bola are mera phone tut gaya. Bholu bola sorry bhai galti se gir gaya. Guddu bola ab me video kaise dekhunga. Bholu bola me apna phone de deta hu. Dono ne milke phone pe cartoon dekha. Dono bahut hasse. Aakhir me dono haste hue ghar gaye."),
        ("Guddu Bholu ka jungle wala safar", "jungle", "Ek din Guddu aur Bholu jungle ghoomne gaye. Jungle me bahut saare janwar the. Bholu bola mujhe sher se dar lag raha hai. Guddu bola dar mat me hu na. Dono ne jungle me bahut masti ki. Dono ne ped ke neeche baith ke samosa khaya. Dono ne photo khinchi. Aakhir me dono haste hue ghar gaye."),
        ("Guddu Bholu ki mela wali masti", "mela", "Ek din Guddu aur Bholu mela ghoomne gaye. Mela me jhoola, golgappe aur khilone the. Guddu ne jhoola jhoola. Bholu ne golgappe khaye. Dono ne khilone kharide. Bholu bola aaj to bahut maza aaya. Guddu bola kal phir aayenge. Dono ne milke samosa khaya. Dono haste hue ghar gaye."),
    ]
    idx = day_num % len(stories)
    top_text, red_word, story = stories[idx]
    print(f"Aaj ki kahani No. {idx+1}/{len(stories)} : {top_text}")
    story += " Subscribe karo."
    title = top_text + " | Guddu Bholu Comedy"
    return title, top_text, red_word, story

title, top_text, red_word, story = get_new_story()
print("TITLE:", title)

# ============ 2. AUDIO - EK BAAR, CARTOON VOICE, REPEAT NAHI ============
from gtts import gTTS
from moviepy.editor import AudioFileClip
os.makedirs("output", exist_ok=True)
gTTS(text=story, lang='hi', slow=False).save("output/audio_raw.mp3")
subprocess.run(["ffmpeg", "-y", "-i", "output/audio_raw.mp3", "-filter:a", "asetrate=44100*1.25,aresample=44100,atempo=0.95", "output/audio.mp3"], check=True)
d = AudioFileClip("output/audio.mp3").duration
print("Audio:", d, "sec - ek hi kahani, repeat nahi, cartoon voice")

# ============ 3. VIDEO - MR COMEDY STYLE ============
W, H = 1080, 1920
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
try:
    font_big = ImageFont.truetype(F, 62)
    font_small = ImageFont.truetype(F, 46)
    font_wait = ImageFont.truetype(F, 50)
except:
    font_big = ImageFont.load_default()
    font_small = font_big
    font_wait = font_big

BGS = [
    ((255, 220, 100), (255, 180, 0), "TOY SHOP"),
    ((180, 220, 255), (100, 160, 255), "PARKING"),
    ((200, 255, 200), (120, 200, 120), "GHAR"),
    ((255, 200, 220), (255, 120, 180), "RESTAURANT"),
    ((255, 240, 180), (200, 160, 80), "SCHOOL"),
    ((220, 220, 255), (140, 140, 255), "MELA"),
]
random.shuffle(BGS)
print("Aaj ka background:", [b[2] for b in BGS])

# POSE - BAAT KE HISAB SE, FALTU NAHI HILEGA
def get_pose(scene_text):
    t = scene_text.lower()
    if "gussa" in t:
        return "gussa"
    if "sorry" in t or "galti" in t:
        return "sorry"
    if "samosa" in t and ("khaya" in t or "kha" in t or "khayenge" in t):
        return "kha_raha"
    if "paise" in t and ("diye" in t or "mil" in t):
        return "khush"
    if "dar" in t:
        return "dar"
    if "has" in t or "maza" in t or "khush" in t or "party" in t or "jeet" in t:
        return "khush"
    if "bola" in t or "samjha" in t:
        return "samjha_raha"
    return "normal"

def draw_full_body(d, cx, cy, col, shirt, name, fr, talk, pose):
    if not talk:
        pose = "normal"
    y = cy
    lean = 0
    if pose == "gussa":
        y = cy + 10
        lean = 15
    elif pose == "dar":
        y = cy + int(math.sin(fr*1.2)*6)
        lean = -10
    elif pose == "khush":
        y = cy + int(math.sin(fr*0.6)*15)
    else:
        y = cy + int(math.sin(fr*0.3)*
