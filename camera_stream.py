import cv2
import time

# Set your camera's IP address, username, and password here
camera_ip = "192.168.1.24"  # Camera's IP address
username = "admin"  # Camera's username
password = "123456"  # Camera's password

# Example RTSP URL format based on the image (Main Stream)
rtsp_url = f"rtsp://{username}:{password}@{camera_ip}:554/h264"

cap = None

# Zoom configuration
zoom_duration = 5  # Time in seconds for each zoom level (zoom in and out)
max_zoom = 2.0     # Maximum zoom factor (2.0 means zoom in 2x)

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
    start_time = time.time()
    zooming_in = True  # Start with zooming in
    zoom_factor = 1.0  # Initial zoom level

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Get frame dimensions
        height, width, _ = frame.shape

        # Calculate time passed
        elapsed_time = time.time() - start_time

        # Toggle zoom direction every zoom_duration seconds
        if elapsed_time > zoom_duration:
            zooming_in = not zooming_in
            start_time = time.time()

        # Adjust zoom factor based on whether zooming in or out
        if zooming_in:
            zoom_factor += 0.01  # Zoom in
            if zoom_factor > max_zoom:
                zoom_factor = max_zoom
        else:
            zoom_factor -= 0.01  # Zoom out
            if zoom_factor < 1.0:
                zoom_factor = 1.0

        # Calculate the crop size based on zoom factor
        crop_width = int(width / zoom_factor)
        crop_height = int(height / zoom_factor)

        # Calculate crop starting point (center the crop)
        x_start = (width - crop_width) // 2
        y_start = (height - crop_height) // 2

        # Crop and resize the frame
        cropped_frame = frame[y_start:y_start + crop_height, x_start:x_start + crop_width]
        resized_frame = cv2.resize(cropped_frame, (width, height))

        # Display the zoomed frame
        cv2.imshow('Camera Stream', resized_frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
