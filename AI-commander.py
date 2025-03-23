import cv2
import numpy as np
import serial
import time
from ultralytics import YOLO

ser = serial.Serial('COM8', 9600, timeout=1)
time.sleep(2)  

model = YOLO("yolov8m.pt")

CAMERA_URL = "http://192.168.1.4:8080/video"  

def capture_frame():
    """Capture a frame from the camera"""
    cap = cv2.VideoCapture(CAMERA_URL)
    time.sleep(1)  
    ret, frame = cap.read()
    cap.release()  
    if not ret:
        print("Error: Failed to capture frame")
        return None
    return frame

def detect_and_count_objects(frame):
    """Run YOLO detection, count objects, and draw bounding boxes"""
    if frame is None:
        return 0, None
    results = model(frame)
    object_count = sum(len(result.boxes) for result in results)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  
            conf = box.conf[0]  
            cls = int(box.cls[0])  
            label = f"{model.names[cls]} {conf:.2f}"  

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return object_count, frame

def send_command(command):
    """Send command to Arduino"""
    ser.write(command.encode())  
    time.sleep(0.1)

previous_cars = 0  
current_lane = 1  

while True:
    input(f"Switch the camera to LANE {current_lane} and press Enter...")  
    frame = capture_frame()  
    car_count, processed_frame = detect_and_count_objects(frame)

    print(f"Lane {current_lane}: {car_count} cars (Previous: {previous_cars} cars)")

    if processed_frame is not None:
        frame_resized = cv2.resize(processed_frame, (800, 600))
        cv2.imshow("YOLO Object Detection", frame_resized)
        cv2.waitKey(1)  

    if car_count > previous_cars:
        if current_lane == 1:
            send_command("LANE1_GREEN")  
        else:
            send_command("LANE2_GREEN")  
        print("Traffic lights switched!")
    else:
        print("No change in traffic lights.")

    previous_cars = car_count
    current_lane = 2 if current_lane == 1 else 1  

    time.sleep(2)

cv2.destroyAllWindows()  
