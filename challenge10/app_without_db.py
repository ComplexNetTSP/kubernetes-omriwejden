from flask import Flask
from datetime import datetime
import socket

app = Flask(__name__)

@app.route("/")
def index():
    # Static information
    my_name = "Wejden"
    project_name = "My Web Project"
    version = "1.0"
    
    # Dynamic information
    hostname = socket.gethostname()  
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    
    # HTML content
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
      </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
