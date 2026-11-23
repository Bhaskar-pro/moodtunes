import os
import sys
import uuid

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), "emotion_model"))
sys.path.append(os.path.join(os.path.dirname(__file__), "database"))
sys.path.append(os.path.join(os.path.dirname(__file__), "music"))

from detector import detect_emotion          # noqa: E402
from db import fetch_songs_by_mood, log_history  # noqa: E402
from music_client import search_track      # noqa: E402

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXT = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """
    Accepts an uploaded image (webcam snapshot or file), detects the emotion,
    fetches matching songs from MySQL, enriches top picks with Spotify data.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400

    filename = secure_filename(f"{uuid.uuid4().hex}_{file.filename}")
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        result = detect_emotion(filepath)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

    if not result["face_found"]:
        return jsonify({"error": "No face detected. Try again with better lighting."}), 200

    mood = result["mood"]
    songs = fetch_songs_by_mood(mood, limit=10)

    enriched = []
    for song in songs:
        music_data = search_track(song.get("spotify_query") or f"{song['title']} {song['artist']}")
        enriched.append({
            "id": song["id"],
            "title": song["title"],
            "artist": song["artist"],
            "mood": song["mood"],
            "music": music_data,
        })
        try:
            log_history(result["emotion"], mood, song["id"])
        except Exception:
            pass  # history logging is non-critical

    return jsonify({
        "emotion": result["emotion"],
        "mood": mood,
        "confidence": result["confidence"],
        "songs": enriched,
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)