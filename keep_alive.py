from flask import Flask
from threading import Thread
from waitress import serve  # Adicionando waitress para manter o Flask ativo

app = Flask(__name__)

@app.route("/")
def home():
    return "Estou online!"

def run():
    serve(app, host="0.0.0.0", port=8080)  # Usando waitress

def keep_alive():
    t = Thread(target=run)
    t.start()
