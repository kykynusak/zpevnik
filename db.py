import psycopg2
from dotenv import load_dotenv
import os

# Načti .env proměnné
load_dotenv()

def get_connection():
    try:
        connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME")
        )
        return connection
    except Exception as e:
        print("❌ Chyba při připojení k DB:", e)
        return None
print("DB_USER:", os.getenv("DB_USER"))
