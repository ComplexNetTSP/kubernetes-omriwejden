from flask import Flask, request
from datetime import datetime
from pymongo import MongoClient
import os

app = Flask(__name__)

# Configuration MongoDB via variables d'environnement
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGO_DB = os.environ.get("MONGO_DB", "mydatabase")

@app.route("/")
def index():
    my_name = "Wejden"
    project_name = "Challenge3"
    version = "V2"
    hostname = request.host_url
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Connexion à MongoDB sans authentification
    client = MongoClient(
        host=MONGO_HOST,
        port=MONGO_PORT
    )
    db = client[MONGO_DB]
    collection = db["requests"]

    # Enregistrer l'adresse IP du client et la date
    client_ip = request.remote_addr
    record = {
        "ip": client_ip,
        "date": datetime.now()
    }
    collection.insert_one(record)

    # Récupérer les 10 derniers enregistrements (triés par date décroissante)
    last_10 = collection.find().sort("date", -1).limit(10)

    # Construire une table HTML avec les 10 derniers enregistrements
    history_html = "<table border=1><tr><th>IP</th><th>Date</th></tr>"
    for doc in last_10:
        history_html += f"<tr><td>{doc['ip']}</td><td>{doc['date']}</td></tr>"
    history_html += "</table>"

    # Contenu HTML principal
    html_content = f"""
    <html>
      <head><title>{project_name} - {version}</title></head>
      <body>
        <h1>Welcome to {project_name}!</h1>
        <p><strong>Name:</strong> {my_name}</p>
        <p><strong>Project Name:</strong> {project_name}</p>
        <p><strong>Version:</strong> {version}</p>
        <p><strong>Hostname:</strong> {hostname}</p>
        <p><strong>Current Date:</strong> {current_date}</p>
        <hr/>
        <h2>Last 10 Access Records</h2>
        {history_html}
      </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
