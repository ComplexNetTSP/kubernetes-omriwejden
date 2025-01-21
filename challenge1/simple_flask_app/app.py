from flask import Flask, request
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__)

# Configuration MongoDB
MONGO_URI = "mongodb://mongodb:27017"  # Connexion via le nom du service MongoDB dans Docker Compose
client = MongoClient(MONGO_URI)
db = client['flask_app_db']
collection = db['requests']

@app.route("/")
def homepage():
    # Enregistrer l'adresse IP du client et la date dans MongoDB
    client_ip = request.remote_addr
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record = {"ip": client_ip, "date": current_date}
    collection.insert_one(record)

    # Récupérer les 10 derniers enregistrements
    last_records = collection.find().sort("_id", -1).limit(10)
    records_html = "".join(
        [f"<p>{record['ip']} - {record['date']}</p>" for record in last_records]
    )

    # Affichage des informations sur la page
    return f"""
        <h1>Your Name: Wejden</h1>
        <h2>Project Name: Simple Flask Web Service</h2>
        <h3>Version: V2</h3>
        <h4>Server Hostname: {request.host}</h4>
        <h5>Current Date: {current_date}</h5>
        <h5>Last 10 Requests:</h5>
        {records_html}
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
