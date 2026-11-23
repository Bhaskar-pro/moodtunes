"""
Train the emotion CNN on FER2013 (folder-structured version).

Expects the dataset extracted at:
    archive/train/<emotion_name>/*.jpg
    archive/test/<emotion_name>/*.jpg

(This is the Kaggle msambare/fer2013 image-folder format, not the CSV format.)

Usage:
    python train.py
"""

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

from model import build_emotion_model, EMOTIONS

TRAIN_DIR = "archive/train"
TEST_DIR = "archive/test"
MODEL_OUT = "emotion_model.h5"
IMG_SIZE = (48, 48)
BATCH_SIZE = 64


def build_generators():
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
    )
    val_datagen = ImageDataGenerator(rescale=1.0 / 255)

    # classes=EMOTIONS forces the folder->label mapping to match model.py's
    # EMOTIONS order exactly (folder names must match those strings, e.g. "happy", "sad").
    train_gen = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        color_mode="grayscale",
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        classes=EMOTIONS,
        shuffle=True,
    )
    val_gen = val_datagen.flow_from_directory(
        TEST_DIR,
        target_size=IMG_SIZE,
        color_mode="grayscale",
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        classes=EMOTIONS,
        shuffle=False,
    )
    return train_gen, val_gen


def main():
    print("Loading FER2013 dataset from folders...")
    train_gen, val_gen = build_generators()

    print("Class indices (must line up with EMOTIONS in model.py):")
    print(train_gen.class_indices)

    model = build_emotion_model()
    model.summary()

    callbacks = [
        ModelCheckpoint(MODEL_OUT, monitor="val_accuracy", save_best_only=True, verbose=1),
        EarlyStopping(monitor="val_loss", patience=8, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=4, min_lr=1e-6),
    ]

    model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=60,
        callbacks=callbacks,
    )

    print(f"Training done. Best model saved to {MODEL_OUT}")


if __name__ == "__main__":
    main()