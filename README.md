# A Raspberry Pi object detection tool with OpenCV, COCO, and Picamera2 

A Raspberry Pi-based system that uses OpenCV and a COCO-trained object detection model to identify pigeons in real-time. When motion is detected by an IR sensor, the camera is activated. If a pigeon is detected in the camera feed, a servo motor is triggered. This can be perfect for automated deterrent systems or research projects.

## Features:

- Real-time object detection using OpenCV and COCO model
- Triggered by an IR motion sensor for power efficiency
- Activates a servo motor when a pigeon is detected
- Specifically monitors for pigeons among other COCO-classified objects
- Runs on a Raspberry Pi (tested on Raspberry Pi 4)

## System Overview

```plaintext
         [ IR Sensor ]
               |
         [ Raspberry Pi ]
         /              \
[ Camera Module ]   [ Servo Motor ]
         |                  ^
[ OpenCV + COCO Model ]     |
         |                  |
Detects "bird" → Verifies Pigeon 
```
