import cv2
import numpy as np
from PIL import Image

def is_image_blurry(image_file, threshold=100.0):
    # Load image from file-like object
    image = Image.open(image_file).convert('L')  # Convert to grayscale
    img_array = np.array(image)
    # Compute the Laplacian variance (sharpness indicator)
    variance = cv2.Laplacian(img_array, cv2.CV_64F).var()
    return variance < threshold, variance
