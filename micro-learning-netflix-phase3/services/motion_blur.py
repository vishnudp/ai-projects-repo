import cv2

def blur_frame(frame):

    return cv2.GaussianBlur(
        frame,
        (7,7),
        0
    )