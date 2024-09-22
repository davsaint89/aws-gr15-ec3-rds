from flask import Flask
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

from routes.route import *


     
if __name__ == "__main__":    
    host = "127.0.0.1"
    port = 8000
    app.run(host, port, True)

 