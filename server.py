from flask import Flask, render_template, request, jsonify
from database.db import *

app = Flask(__name__)

@app.route('/activity_log')
def register_page():
    #connection_SQL()
    return render_template("register.html")

@app.route('/submit', methods=["post"])
def register_user():
    try:
        # Extract form data
        data = request.form

        # Extract data
        activity_name = data['activityName']
        description = data['description']
        start_date = data['startDate']
        end_date = data['endDate']

        # Attempt to insert the data into the database
        if insert(activity_name, description, start_date, end_date):
            return jsonify({"message": "Activity submitted successfully"}), 200
        else:
            return jsonify({"error": "Failed to submit activity"}), 500
    except Exception as err:
        return jsonify({"error": f"An error occurred: {err}"}), 500
    
    
     
if __name__ == "__main__":    
    host = "127.0.0.1"
    port = 8000
    app.run(host, port, True)

 