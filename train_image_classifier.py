# train_image_classifier.py
import os
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Hyperparameters
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5

# Path to your dataset folder
DATASET_PATH = 'dataset'
MODEL_OUT_PATH = 'saved_model/my_scrap_cnn'

# Data generators for training and validation
train_datagen = ImageDataGenerator(
  rescale=1./255,
  validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

val_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# Model definition
model = models.Sequential([
    layers.Input(shape=(*IMAGE_SIZE, 3)),
    layers.Conv2D(32, (3,3), activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(train_generator.num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Training
model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS
)

# Save the trained model
MODEL_OUT_PATH = 'saved_model/my_scrap_cnn.keras'
os.makedirs(os.path.dirname(MODEL_OUT_PATH), exist_ok=True)
model.save(MODEL_OUT_PATH)
print(f"Model trained and saved at: {MODEL_OUT_PATH}")
