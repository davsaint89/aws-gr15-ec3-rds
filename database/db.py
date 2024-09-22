import os
from dotenv import load_dotenv
import pymysql

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
passw = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

def connection_SQL():
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=passw,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor  # Ensure DictCursor is used
        )
        print("Succesfull connection to database")
        return connection
    except Exception as err:
        print("Error", err)
        return None



def insert(name, description, startDate, endDate):
    try:
        # Create a connection to the database
        connection = connection_SQL()

        # Use a parameterized query to avoid SQL injection
        instruction = """
            INSERT INTO work_activity_log (activity_name, description, start_date, end_date)
            VALUES (%s, %s, %s, %s);
        """

        with connection.cursor() as cursor:
            # Execute the parameterized query with the provided values
            cursor.execute(instruction, (name, description, startDate, endDate))
        
        # Commit the transaction
        connection.commit()

        # Return success
        print("Record inserted successfully")
        return True
    except pymysql.MySQLError as err:
        # Handle MySQL-specific errors
        print(f"MySQL Error: {err}")
        return False
    except Exception as err:
        # Handle general errors
        print(f"Error: {err}")
        return False
    finally:
        # Ensure the connection is closed
        connection.close()
