import base64
import numpy as np
import cv2
import face_recognition
from io import BytesIO

class Images:

    @staticmethod
    def convert_and_upscale_image(byte):
        if isinstance(byte, str):
            # Decode base64 data into image bytes
            byte = byte.split(",")[1]
            image_bytes = base64.b64decode(byte)

            # Convert image bytes to numpy array
            image_array = np.frombuffer(image_bytes, np.uint8)

            # Decode the numpy array into an image
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            # Get original dimensions
            height, width, _ = image.shape

            # Define the upscale factor (e.g., 2x)
            upscale_factor = 4

            # Calculate new dimensions
            new_height = height * upscale_factor
            new_width = width * upscale_factor

            # Upscale the image
            upscaled_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        else:
            upscaled_image = face_recognition.load_image_file(BytesIO(byte))

        return upscaled_image