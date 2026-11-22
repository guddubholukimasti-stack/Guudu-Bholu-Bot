from flask import Flask, jsonify
import random, datetime, hashlib

app = Flask(__name__)

def kahani_banao():
    today = str(datetime.date.today())
    seed = int(hashlib.md5(today.encode()).hexdigest(), 16) % 10000
    random.seed(seed)
    guddu = random.choice([
        "Bholu, aaj maine samosa laya hai!",
        "Bholu, aaj video banana hai, jaldi uth!",
        "Bholu, aaj Lala ne bola hai viral video banana hai!",
        "Bholu, aaj 9 baje Mission ON hai!"
    ])
    bholu = random.choice([
        "Guddu, mujhe 9 baje uthana, main so raha hu!",
        "Samosa kahan hai? Mujhe to dikha hi nahi!",
        "Maine nahi khaya, ye to hawa me udd gaya!",
        "Guddu, pehle samosa de, fir video banayenge!"
    ])
    chintu = random.choice([
        "Main aa gaya! Chintu is here!",
        "Mujhe bhi samosa chahiye!",
        "Chalo, aaj ka video main banata hu!"
    ])
    twist = random.choice([
        "Plate khaali nikli! Samosa gayab!",
        "Bholu ke muh me samosa tha, pakda gaya!",
        "Chintu ne chupke se samosa kha liya!"
    ])
    random.seed()
    kahani = "Guddu: " + guddu + " Bholu: " + bholu + " Chintu: " + chintu + " Twist: " + twist + " End: Lala, comment me batao, Samosa kisne khaya?"
    return kahani

@app.route('/')
def home():
    kahani = kahani_banao()
    return "<h1>LALA MISSION 9 BAJE - FULL AUTO ON</h1><p>" + kahani + "</p><p><a href='/run-auto'>AUTO CHALAO</a></p>"

@app.route('/run-auto')
def run_auto():
    kahani = kahani_banao()
    return jsonify({"status": "FULL AUTO HO GAYA", "kahani": kahani, "date": str(datetime.date.today())})

@app.route('/today')
def today():
    return jsonify({"kahani": kahani_banao(), "date": str(datetime.date.today())})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
