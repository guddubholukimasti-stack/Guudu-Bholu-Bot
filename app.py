from flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

HTML = """
<h1 style="text-align:center;">🤖 GUDDU-BHOLOU BOT LIVE HAI!</h1>
<p style="text-align:center;">LALA MISSION 9 BAJE - ON HAI!</p>
<div style="text-align:center;">
<input id="msg" placeholder="Guddu se kuch bolo..." style="padding:10px; width:70%;">
<button onclick="send()" style="padding:10px;">Bhejo</button>
<p id="reply"></p>
</div>
<script>
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

@app.route('/chat', methods=['POST'])
def chat():
    msg = request.json.get('msg','').lower()
    if 'samosa' in msg:
        reply = "Arre Lala! Samosa sunte hi Bholu ke muh me paani aa gaya! Bholu bola - Ek khaunga, baaki sab chhupa dunga!"
    elif 'bholu' in msg:
        reply = "Bholu to abhi so raha hai! Usne bola - Guddu, mujhe 9 baje uthana, video banani hai!"
    elif 'hi' in msg or 'hello' in msg or 'hey' in msg:
        reply = "Haan Malik! Main Guddu hu! LALA MISSION 9 BAJE ON hai! Bol, kya video banau aaj?"
    elif 'video' in msg:
        reply = "Video to main roz 9 baje bana dunga! Tu bas Malik banke views ginna!"
    else:
        reply = random.choice([
            "Hahaha! Ye to mast bola Lala! Bholu ko batata hu, wo bhi hasega!",
            "Arre wah! Tu to bada chalak nikla! Chal, ispe ek video bana dete hai!",
            "Samajh gaya Malik! Ye wali baat kal ki kahani me dal deta hu!"
        ])
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
