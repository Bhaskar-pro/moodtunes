"""
Detects faces in an image using OpenCV's Haar Cascade,
then runs the trained CNN to predict the emotion for the largest face.
"""

import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model

from model import EMOTIONS, EMOTION_TO_MOOD

MODEL_PATH = os.path.join(os.path.dirname(__file__), "emotion_model.h5")
CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

_model = None
_face_cascade = None


def _load_resources():
    global _model, _face_cascade
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}. Run train.py first, "
                "or drop a pretrained emotion_model.h5 here."
            )
        _model = load_model(MODEL_PATH)
    if _face_cascade is None:
        _face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    return _model, _face_cascade


def detect_emotion(image_path):
    """
    Takes a path to an image file, returns:
    {
        "emotion": "Happy",
        "mood": "happy",
        "confidence": 0.87,
        "face_found": True
    }
    """
    model, face_cascade = _load_resources()

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image file.")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(48, 48))

    if len(faces) == 0:
        return {"emotion": None, "mood": "calm", "confidence": 0.0, "face_found": False}

    # Pick the largest detected face
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    face_roi = gray[y:y + h, x:x + w]
    face_roi = cv2.resize(face_roi, (48, 48))
    face_roi = face_roi.astype("float32") / 255.0
    face_roi = np.expand_dims(face_roi, axis=(0, -1))  # shape (1, 48, 48, 1)

    preds = model.predict(face_roi, verbose=0)[0]
    idx = int(np.argmax(preds))
    emotion = EMOTIONS[idx]
    confidence = float(preds[idx])
    mood = EMOTION_TO_MOOD[emotion]

    return {
        "emotion": emotion,
        "mood": mood,
        "confidence": round(confidence, 3),
        "face_found": True,
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python detector.py <image_path>")
    else:
        print(detect_emotion(sys.argv[1]))