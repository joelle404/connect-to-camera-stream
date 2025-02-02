import torch
import cv2
from pathlib import Path
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.torch_utils import select_device
from yolov5.utils.general import non_max_suppression, scale_coords
from yolov5.utils.dataloaders import LoadStreams

# Load YOLOv5 model
weights = "best.pt"  # Path to your trained model
device = select_device('')  # Automatically select GPU or CPU
model = DetectMultiBackend(weights, device=device, dnn=False)
stride, names, pt = model.stride, model.names, model.pt

# IP Camera RTSP URL
rtsp_url = "rtsp://admin:123456@192.168.1.24:554/h264"

# Load video stream
dataset = LoadStreams(rtsp_url, img_size=640, stride=stride, auto=pt)

# Run inference
model.warmup(imgsz=(1, 3, 640, 640))  # Warmup model
for path, img, im0s, vid_cap, s in dataset:
    img = torch.from_numpy(img).to(device)
    img = img.float() / 255.0  # Normalize
    if len(img.shape) == 3:
        img = img[None]  # Expand for batch dimension

    # Inference
    pred = model(img)

    # Apply Non-Maximum Suppression (NMS)
    pred = non_max_suppression(pred, 0.5, 0.45)

    # Process detections
    for det in pred:
        im0 = im0s.copy()
        if len(det):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
            for *xyxy, conf, cls in det:
                label = f"{names[int(cls)]} {conf:.2f}"
                cv2.rectangle(im0, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2)
                cv2.putText(im0, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('YOLOv5 Camera Stream', im0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
