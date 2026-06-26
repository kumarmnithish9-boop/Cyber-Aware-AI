import cv2
import numpy as np

def read_qr(image):

    image_np = np.array(image)

    detector = cv2.QRCodeDetector()

    data, _, _ = detector.detectAndDecode(
        image_np
    )

    if data:
        return data

    return "No QR code detected"