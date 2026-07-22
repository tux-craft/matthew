#!/bin/python3

# PREREQUISITES
# apt install python3-opencv python3-picamera2

import cv2
from picamera2 import Picamera2
from libcamera import Transform
import time
from datetime import datetime

# VARIABLES
dir_pics = "/home/tux-craft/matthew/pictures"

picam2 = Picamera2()
camera_config = picam2.create_video_configuration(main={"size": (640, 480)}, transform=Transform(vflip=0))
picam2.configure(camera_config)
picam2.start()

prev_frame = None
motion_detected = False

while True:
    frame = picam2.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if prev_frame is None:
        prev_frame = gray
        continue

    frame_delta = cv2.absdiff(prev_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 500: # Adjust area threshold
            motion_detected = True
            break

    if motion_detected:
        timestamp = datetime.now().strftime('%Y%m%d-%H:%M:%S.%f')
        filename = f"{dir_pics}/motion_{timestamp}.jpg"
        # Use libcamera-still or picamera2.capture_file() to save image
        print(f"Motion detected! Saving {filename}")
        picam2.capture_file(filename) 
        motion_detected = False # Reset after detection or add delay

    prev_frame = gray
    time.sleep(0.1) # Small delay
