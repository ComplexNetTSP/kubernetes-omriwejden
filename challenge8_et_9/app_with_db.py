from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGO_DB = os.environ.get("MONGO_DB", "mydatabase")

@app.route("/")
def index():
    client_ip = request.remote_addr
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Connexion à MongoDB
    client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
    db = client[MONGO_DB]
    collection = db["requests"]
    collection.insert_one({"ip": client_ip, "time": current_time})

    # Récupérer les 10 derniers enregistrements
    records = collection.find().sort("time", -1).limit(10)
    history = "\n".join([f"{r['ip']} - {r['time']}" for r in records])

    # Récupérer le nom du pod depuis la variable d'environnement HOSTNAME
    pod_name = os.environ.get("HOSTNAME", "Unknown Pod")

    return f"""
    <h1>Flask App with MongoDB</h1>
    <p>Client IP: {client_ip}</p>
    <p><strong>Pod Name:</strong> {pod_name}</p>
    <p>Current Time: {current_time}</p>
    <p><strong>Last 10 Records:</strong></p>
    <pre>{history}</pre>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
