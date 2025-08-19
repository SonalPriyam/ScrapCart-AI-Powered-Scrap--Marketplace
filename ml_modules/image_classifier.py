import numpy as np
from PIL import Image
import tensorflow as tf
import os
import zipfile
import tarfile

# SETTINGS
ZIP_PATH = 'saved_model/my_scrap_cnn.zip'   # Change to .tar.gz if you use tar
TAR_PATH = 'saved_model/my_scrap_cnn.tar.gz'  # Only if you choose tar.gz
MODEL_PATH = 'saved_model/my_scrap_cnn.keras'
CLASS_NAMES = ['Clothes', 'e waste', 'Glass', 'metal', 'others', 'paper', 'plastic']  # Update if your folder names change

def ensure_model_extracted():
    # Try unzip first (default)
    if not os.path.exists(MODEL_PATH) and os.path.exists(ZIP_PATH):
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(MODEL_PATH))
    # Try untar if needed (if you use tar.gz)
    if not os.path.exists(MODEL_PATH) and os.path.exists(TAR_PATH):
        with tarfile.open(TAR_PATH, 'r:gz') as tar_ref:
            tar_ref.extractall(os.path.dirname(MODEL_PATH))

# Run extraction before loading
ensure_model_extracted()
model = tf.keras.models.load_model(MODEL_PATH)

def preprocess_image(image_file):
    img = Image.open(image_file).convert('RGB')
    img = img.resize((224, 224))  # match training script
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_scrap_type(image_file):
    img_array = preprocess_image(image_file)
    predictions = model.predict(img_array)
    predicted_idx = np.argmax(predictions, axis=1)[0]
    return CLASS_NAMES[predicted_idx]
