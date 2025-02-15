import cv2
import numpy as np


def save_image(image, path):
    image_np = cv2.cvtColor(np.array(image), (cv2.COLOR_RGB2BGR if image.mode == "RGB" else cv2.COLOR_GRAY2BGR))

    print(f"Saving to {path}...")
    cv2.imwrite(path, image_np)
    print("Saved successfully.")
