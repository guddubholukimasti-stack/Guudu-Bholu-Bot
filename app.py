from flask import Flask, request, jsonify
app = Flask(__name__)

def guddu_reply(msg):
    m = msg.lower()
    if "hi" in m or "hello" in m:
        return "Arre aa gaya mera bhai! Guddu Bholu yaha hai! Bol kya haal hai?"
    if "naam" in m or "kaun" in m:
        return "Main Guddu Bholu hu! Lala Mission pe hu!"
    if "bye" in m:
        return "Arre ruk ja yaar, abhi to aaya hai!"
    return "Samajh gaya! Tune bola - " + msg + " - Aur bata?"

@app.route("/")
def home():
    html = "<html><head><meta name=viewport content=width=device-width,initial-scale=1>"
    html += "<style>body{font-family:sans-serif;background:#111;color:white;padding:10px}h2{text-align:center;color:#ffcc00}#box{height:70vh;overflow-y:auto;background:#222;padding:10px;border-radius:10px}.me{text-align:right;color:#00ff88;margin:8px}.bot{color:#ffcc00;margin:8px}input{width:75%;padding:12px;border-radius:10px;border:none}button{width:20%;padding:12px;background:#ffcc00;border:none;border-radius:10px}</style></head>"
    html += "<body><h2>Guddu Bholu - Lala Mission ON</h2>"
    html += "<div id=box><div class=bot><b>Guddu:</b> Aa gaya! Bol kya baat hai?</div></div><br>"
    html += "<input id=m placeholder=Yaha-likh><button onclick=send()>Bhej</button>"
    html += "<script>async function send(){let inp=document.getElementById('m');let txt=inp.value;if(!txt)return;let box=document.getElementById('box');box.innerHTML+='<div class=me><b>Tu:</b> '+txt+'</div>';inp.value='';let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({msg:txt})});let d=await r.json();box.innerHTML+='<div class=bot><b>Guddu:</b> '+d.reply+'</div>';box.scrollTop=box.scrollHeight;}</script></body></html>"
    return html

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("msg", "")
    return jsonify({"reply": guddu_reply(msg)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
