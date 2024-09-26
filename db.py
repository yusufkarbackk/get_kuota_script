from math import pi
import mysql.connector
from mysql.connector import Error


def connect_to_mysql():
    try:
        # Establish a connection
        connection = mysql.connector.connect(
            host="localhost",  # Hostname of the MySQL server (e.g., 'localhost')
            database="telkom_db",  # Database name to connect to
            user="root",  # Your MySQL username
            password="root",
            port=8889,
        )
        print("connected to database")
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")


def update_client_data(newKuota, nomor):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE 'clients' SET 'quota'=(%s), 'last_update'=NOW() WHERE 'nomor'=(%s)
            """,
            (newKuota, nomor),
        )
        conn.commit()
        print(f"sukses update: {nomor}")
    except Error as e:
        conn.rollback()
        print(f"error: {e}")
    finally:
        conn.close()
