from flask import Flask, request, jsonify, render_template_string
import random, datetime
app = Flask(__name__)

def auto_kahani_banao():
    guddu_lines = [
        "Bholu, aaj maine samosa laya hai!",
        "Bholu, aaj video banana hai, jaldi uth!",
        "Bholu, aaj Lala ne bola hai viral video banana hai!",
        "Bholu, aaj 9 baje Mission ON hai!",
        "Bholu, aaj hum YouTube pe chha jayenge!"
    ]
    bholu_lines = [
        "Guddu, mujhe 9 baje uthana, main so raha hu!",
        "Samosa kahan hai? Mujhe to dikha hi nahi!",
        "Maine nahi khaya, ye to hawa me udd gaya!",
        "Guddu, pehle samosa de, fir video banayenge!",
        "Arre Guddu, neend me hi samosa kha gaya kya?"
    ]
    twist = [
        "Plate khaali nikli! Samosa gayab!",
        "Bholu ke muh me samosa tha, pakda gaya!",
        "Dono ne mil ke samosa kha liya aur hasne lage!",
        "Samosa actually Lala ne kha liya tha!",
        "Bholu ne sapne me samosa kha liya tha!"
    ]
    kahani = "Guddu: " + random.choice(guddu_lines) + "\nBholu: " + random.choice(bholu_lines) + "\nTwist: " + random.choice(twist) + "\nEnd: Lala, comment me batao - Samosa kisne khaya?"
    return kahani

HTML = """
<h1 style="text-align:center;">🤖 GUDDU-BHOLOU AUTO FACTORY</h1>
<p style="text-align:center;">LALA MISSION 9 BAJE - AUTO SYSTEM ON HAI!</p>
<div style="text-align:center;">
<button onclick="auto()" style="padding:12px; background:green; color:white;">🔥 AAJ KI KAHANI AUTO BANAO</button>
<p id="k" style="white-space:pre-line; font-size:18px;"></p>
<br>
<input id="msg" placeholder="Guddu se kuch bolo..." style="padding:10px; width:70%;">
<button onclick="send()" style="padding:10px;">Bhejo</button>
<p id="reply"></p>
</div>
<script>
async function auto(){
  let r = await fetch('/auto');
  let d = await r.json();
  document.getElementById('k').innerText = "Aaj Ki Kahani:\\n" + d.kahani + "\\n\\nDate: " + d.date;
}
async function send(){
  let m = document.getElementById('msg').value;
  let r = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({msg:m})});
  let d = await r.json();
  document.getElementById('reply').innerText = "Guddu: " + d.reply;
}
</script>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/auto')
def auto():
    return jsonify({"kahani": auto_kahani_banao(), "date": str(datetime.date.today()), "status": "AUTO SYSTEM NE BANA DIYA"})

@app.route('/chat', methods=['POST'])
def chat():
    msg = request.json.get('msg','').lower()
    if 'samosa' in msg:
        reply = "Arre Lala! Samosa sunte hi Bholu ke muh me paani aa gaya!"
    elif 'bholu' in msg:
        reply = "Bholu to abhi so raha hai! Usne bola - Guddu, mujhe 9 baje uthana!"
    elif 'hi' in msg or 'hello' in msg or 'hey' in msg:
        reply = "Haan Malik! Main Guddu hu! LALA MISSION 9 BAJE ON hai!"
    else:
        reply = random.choice(["Hahaha! Ye to mast bola Lala!", "Samajh gaya Malik! Kal ki kahani me dal deta hu!"])
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
