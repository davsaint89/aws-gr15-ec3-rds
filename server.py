from flask import Flask, render_template, request
#from database.db import *

app = Flask(__name__)

@app.route('/activity_log')
def register_page():
    return render_template("register.html")

@app.route('/submit', methods=["post"])
def register_user():
    data = request.form
    print(data)

    return "Activity added"
     
if __name__ == "__main__":    
    host = "127.0.0.1"
    port = 8000
    app.run(host, port, True)

    