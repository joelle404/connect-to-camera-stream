import cv2
import time

# Set your camera's IP address, username, and password here
camera_ip = "192.168.1.24"  # Camera's IP address
username = "admin"  # Camera's username
password = "123456"  # Camera's password

# Example RTSP URL format based on the image (Main Stream)
rtsp_url = f"rtsp://{username}:{password}@{camera_ip}:554/h265"

cap = None

# Try to open the stream up to 5 times with a delay between each attempt
attempts = 5
for attempt in range(attempts):
    cap = cv2.VideoCapture(rtsp_url)
    if cap.isOpened():
        print(f"Successfully connected to the camera on attempt {attempt + 1}")
        break
    else:
        print(f"Attempt {attempt + 1} failed, retrying in 5 seconds...")
        time.sleep(5)

if not cap or not cap.isOpened():
    print("Error: Could not connect to camera.")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow('Camera Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()   