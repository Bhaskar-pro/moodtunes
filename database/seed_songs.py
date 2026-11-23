"""
Populates the songs table with a curated list across 4 moods.
Run: python seed_songs.py
"""

from db import get_connection

SEED_SONGS = [
    # Happy
    ("Kar Gayi Chull", "Badshah, Neha Kakkar", "happy", "hindi", "Kar Gayi Chull Badshah"),
    ("Uptown Funk", "Bruno Mars", "happy", "english", "Uptown Funk Bruno Mars"),
    ("London Thumakda", "Labh Janjua", "happy", "hindi", "London Thumakda"),
    ("Happy", "Pharrell Williams", "happy", "english", "Happy Pharrell Williams"),
    ("Badtameez Dil", "Benny Dayal", "happy", "hindi", "Badtameez Dil"),

    # Sad
    ("Channa Mereya", "Arijit Singh", "sad", "hindi", "Channa Mereya Arijit Singh"),
    ("Someone Like You", "Adele", "sad", "english", "Someone Like You Adele"),
    ("Agar Tum Saath Ho", "Alka Yagnik, Arijit Singh", "sad", "hindi", "Agar Tum Saath Ho"),
    ("Fix You", "Coldplay", "sad", "english", "Fix You Coldplay"),
    ("Tum Hi Ho", "Arijit Singh", "sad", "hindi", "Tum Hi Ho Arijit Singh"),

    # Calm
    ("Kun Faya Kun", "A.R. Rahman", "calm", "hindi", "Kun Faya Kun"),
    ("Weightless", "Marconi Union", "calm", "english", "Weightless Marconi Union"),
    ("Tum Se Hi", "Mohit Chauhan", "calm", "hindi", "Tum Se Hi Mohit Chauhan"),
    ("River Flows in You", "Yiruma", "calm", "instrumental", "River Flows in You Yiruma"),
    ("Ilahi", "Arijit Singh", "calm", "hindi", "Ilahi Arijit Singh"),

    # Energetic
    ("Malhari", "Vishal Dadlani", "energetic", "hindi", "Malhari Vishal Dadlani"),
    ("Believer", "Imagine Dragons", "energetic", "english", "Believer Imagine Dragons"),
    ("Zinda", "Siddharth Mahadevan", "energetic", "hindi", "Zinda Bhaag Milkha Bhaag"),
    ("Eye of the Tiger", "Survivor", "energetic", "english", "Eye of the Tiger Survivor"),
    ("Sultan", "Sukhwinder Singh", "energetic", "hindi", "Sultan Title Track"),
]


def seed():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO songs (title, artist, mood, language, spotify_query) VALUES (%s, %s, %s, %s, %s)",
        SEED_SONGS,
    )
    conn.commit()
    print(f"Inserted {cursor.rowcount} songs.")
    cursor.close()
    conn.close()


if __name__ == "__main__":
    seed()