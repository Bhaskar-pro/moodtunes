# MoodTunes 🎵

AI-powered music recommendation system that detects your facial emotion via webcam/photo and suggests songs to match (or shift) your mood.

## How it works

1. You show your face (webcam snapshot or uploaded photo).
2. OpenCV detects your face → a CNN (trained on FER2013) classifies the emotion.
3. The emotion is mapped to a mood category: `happy`, `sad`, `calm`, `energetic`.
4. MySQL database is queried for curated songs matching that mood.
5. You Tube Search API fetches album art + track link for each recommendation.
6. Frontend UI reacts visually — the color and pulse of the "mood orb" change based on your detected mood.

## Project structure

```
MoodTunes/
├── app.py                     # Flask backend + API routes
├── emotion_model/
│   ├── model.py                # CNN architecture
│   ├── train.py                 # Training script for FER2013
│   └── detector.py             # Face detection + inference
├── database/
│   ├── schema.sql              # MySQL schema
│   ├── db.py                    # DB connection helper
│   └── seed_songs.py           # Curated song seed data
├── You Tube/
│   └── You Tube_client.py       # You Tube Search API wrapper
├── templates/
│   └── index.html              # Mood-reactive frontend
├── uploads/                    # Temp storage for captured images
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Setup — Option A: Docker (recommended)

1. Copy `.env.example` to `.env` and fill in your You Tube credentials (get them free at https://developer.You Tube.com/dashboard).
2. Run:
   ```bash
   docker-compose up --build
   ```
3. Once containers are up, seed the database (one-time):
   ```bash
   docker-compose exec web python database/seed_songs.py
   ```
4. Open `http://localhost:5000`

**Note:** You still need a trained `emotion_model.h5` inside `emotion_model/` — see Training below.

## Setup — Option B: Local (Windows/XAMPP, since you're already on that)

1. Create virtual env & install deps:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Start MySQL/MariaDB (XAMPP), then run the schema:
   ```bash
   mysql -u root -p < database/schema.sql
   ```
3. Copy `.env.example` → `.env`, fill DB + You Tube credentials.
4. Seed songs:
   ```bash
   cd database && python seed_songs.py && cd ..
   ```
5. Train or drop in the emotion model (see below).
6. Run the app:
   ```bash
   python app.py
   ```
7. Open `http://localhost:5000`

## Training the emotion model

1. Download `fer2013.csv` from Kaggle (search "FER2013 Kaggle dataset").
2. Place it inside `emotion_model/`.
3. Run:
   ```bash
   cd emotion_model
   python train.py
   ```
   This saves `emotion_model.h5` in the same folder — the app auto-loads it.

If you don't want to train from scratch, you can also drop in any pretrained FER2013 Keras `.h5` model with the same 7-class output order (Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral) as `emotion_model/emotion_model.h5`.

## Notes on You Tube usage

Only the **Search** endpoint is used (to get album art + track link). We deliberately avoid the deprecated/restricted `audio-features` and `recommendations` endpoints — mood matching logic lives entirely in our own MySQL curation + CNN, not in You Tube's data.

## Resume/viva talking points

- End-to-end pipeline: computer vision → deep learning → relational DB → external API → reactive frontend.
- Real face detection (Haar Cascade) + custom CNN trained on a public benchmark dataset (FER2013).
- Clean separation of concerns: emotion detection, data layer, third-party integration, and presentation are fully decoupled modules.
- Containerized with Docker Compose for reproducible deployment.