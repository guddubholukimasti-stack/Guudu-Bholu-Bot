import os,datetime,json
from PIL import Image,ImageDraw
from gtts import gTTS
from moviepy.editor import *
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
J=[("Ghar todne ka kaam", ["Bhaiya ghar todne ke liye labour chahiye.","Ye lo meri biwi ko le jao.","Ye ghar todegi?","Ye zubaan se hi ghar tod deti hai."]),("Samosa chor", ["Bhaiya samosa kitne ka hai?","20 rupaye ka.","To 10 ka de do.","Aadha kaise du?","Aadha kha ke de do."])]
t,D=J[datetime.datetime.now().timetuple().tm_yday%2]
os.makedirs("o",exist_ok=True)
C=[]
for l in D:
 gTTS(l,lang="hi").save("o/a.mp3");a=AudioFileClip("o/a.mp3");im=Image.new("RGB",(1080,1920),(135,206,235));d=ImageDraw.Draw(im);d.rectangle([0,1000,1080,1920],fill=(255,200,0));d.text((100,1100),l,fill=(0,0,0));im.save("o/f.jpg");C.append(ImageClip("o/f.jpg").set_duration(a.duration).set_audio(a))
V=concatenate_videoclips(C);V.write_videofile("o/f.mp4",fps=24,codec="libx264",audio_codec="aac")
y=build("youtube","v3",credentials=Credentials.from_authorized_user_info(json.loads(os.environ["YOUTUBE_TOKEN"])))
b={"snippet":{"title":t+" #Shorts","description":" ".join(D),"categoryId":"24"},"status":{"privacyStatus":"public","madeForKids":True}}
print(y.videos().insert(part="snippet,status",body=b,media_body=MediaFileUpload("o/f.mp4")).execute()["id"])
