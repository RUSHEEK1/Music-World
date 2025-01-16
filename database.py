import mysql.connector

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",          # Replace with your MySQL server host (e.g., localhost or IP address)
            user="root",       # Replace with your MySQL username
            password="root",   # Replace with your MySQL password
            database="media_player"  # Replace with your database name (e.g., media_player_db)
        )
        if connection.is_connected():
            print("Connection successful!")
            connection.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

connect_to_db()
