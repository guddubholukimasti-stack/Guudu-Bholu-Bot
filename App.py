from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Guddu Bholu Bot LIVE Hai! Lala Mission ON!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
