import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

_pool = None


def get_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="moodtunes_pool",
            pool_size=5,
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "moodtunes"),
        )
    return _pool


def get_connection():
    return get_pool().get_connection()


def fetch_songs_by_mood(mood, limit=10):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM songs WHERE mood = %s ORDER BY RAND() LIMIT %s",
        (mood, limit),
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def log_history(detected_emotion, detected_mood, song_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO history (detected_emotion, detected_mood, song_id) VALUES (%s, %s, %s)",
        (detected_emotion, detected_mood, song_id),
    )
    conn.commit()
    cursor.close()
    conn.close()