from flask import render_template, request, jsonify, get_flashed_messages, redirect, flash, url_for
from server import app
from database.db import *
from controllers.admin_s3 import *
bucket_name = "gr15"
S3_REGION = "us-east-2"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/activity_log')
def register_page():
    #connection_SQL()
    return render_template("register.html")


@app.route('/consult')
def consult_page():
    connection = connection_SQL()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM work_activity_log"
            cursor = connection.cursor()
            cursor.execute(sql)
            activities = cursor.fetchall()  # Retrieve all the data
            print(activities)
        return render_template("activities.html", activities=activities)
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
    finally:
        connection.close()


@app.route('/submit', methods=["post"])
def register_user():
    try:
        # Extract form data
        data = request.form

        # Extract file
        file = request.files
        photo = file['photo']


        # Extract data
        activity_name = data['activityName']
        description = data['description']
        start_date = data['startDate']
        end_date = data['endDate']

        if not insert(activity_name, description, start_date, end_date):
            return jsonify({"error": "Failed to submit activity"}), 500
        flash("Activity submitted successfully!", "success")
        # Save the photo
        session_s3 = connectionS3()
        photo_path, photo_name = save_file(activity_name, photo)
        # Upload the photo
        upload_file_s3(session_s3, photo_path, photo_name)
        # Redirect to the activity
        return redirect('/consult')
    except Exception as err:
        return jsonify({"error": f"An error occurred: {err}"}), 500
    



@app.route('/search_activity', methods=['GET', 'POST'])
def search_activity():
    session_s3 = connectionS3()
    if request.method != 'POST':
        return render_template("search.html")
    search_term = request.form.get('search_term')
    connection = connection_SQL()
    try:
        with connection.cursor() as cursor:
            # Search by ID or Name
            sql = """
                    SELECT * FROM work_activity_log
                    WHERE id = %s OR activity_name LIKE %s
                """
            cursor.execute(sql, (search_term, f"%{search_term}%"))
            activities = cursor.fetchall()  # Get all matching activities
            # Initialize activity image URL
            activity_image_url = None
            # Iterate over the matching activities and search for an image in S3
            for activity in activities:
                print(activity)
                try:
                    activity_name = activity['activity_name']
                    
                    s3_key = f"images/{activity_name}.png"  # Assuming image extension is jpg
                    session_s3.meta.client.head_object(Bucket=bucket_name, Key=s3_key)
                    
                    # If image exists, construct its URL
                    activity_image_url = f"https://{bucket_name}.s3.{S3_REGION}.amazonaws.com/{s3_key}"
                    print(activity_image_url)
                    break  # Stop once we find a matching image
                except session_s3.meta.client.exceptions.ClientError as e:
                    # If no image found, continue searching other activities
                    pass

        return render_template("search_results.html", activities=activities, image_url=activity_image_url)
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500
    finally:
        connection.close()


