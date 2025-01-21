from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
    <h1>Flask App without MongoDB</h1>
    <p>Current Time: {current_time}</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
