from flask import Flask
import random
from gtts import gTTS
from PIL import Image, ImageDraw
from moviepy.editor import ImageClip, AudioFileClip

app = Flask(__name__)

def get_story():
    stories = [
        "Guddu ne Bholu se kaha, aaj samosa free hai! Bholu daud ke gaya, waha Chintu pehle se khada tha! Fir teeno me samose ke liye ladai ho gayi!",
        "Bholu ne Guddu ka samosa chura liya! Guddu bola, mera samosa wapas kar! Chintu bola, dono ka aadha-aadha kar lo! Fir teeno ne mil ke kha liya!",
        "Guddu bola, aaj main YouTube star banunga! Bholu bola, pehle samosa toh khila! Chintu hasne laga, tum dono se na ho payega!"
    ]
    return random.choice(stories)

def make_video(story, num):
    tts = gTTS(text=story, lang='hi')
    tts.save("voice.mp3")
    img = Image.new('RGB', (1080, 1920), color=(255, 200, 0))
    d = ImageDraw.Draw(img)
    d.text((80, 800), "GUDDU BHOLU", fill=(0, 0, 0))
    d.text((80, 900), "Samosa Mission", fill=(0, 0, 0))
    img.save("frame.jpg")
    audio = AudioFileClip("voice.mp3")
    clip = ImageClip("frame.jpg").set_duration(audio.duration).set_audio(audio)
    clip.write_videofile(f"video_{num}.mp4", fps=24, codec='libx264', audio_codec='aac')
    return f"video_{num}.mp4"

@app.route('/')
def home():
    return "Lala Mission ON Hai! Video System Ready!"

@app.route('/run-auto')
def run_auto():
    story = get_story()
    video = make_video(story, random.randint(1, 1000))
    return f"KAHANI: {story} <br> VIDEO BAN GAYA: {video} <br> Ab YouTube Key lagate hi ye auto upload hoga!"

if __name__ == '__main__':
    app.run()
