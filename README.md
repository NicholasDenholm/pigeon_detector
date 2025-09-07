# A Raspberry Pi object detection tool with OpenCV and COCO

A Raspberry Pi-based system that uses OpenCV and a COCO-trained object detection model to identify pigeons in real-time. When motion is detected by an IR sensor, the camera is activated. If a bird type  object is detected in the camera feed, a servo motor is triggered. This can be perfect for automated deterrent systems or research projects.

![pigeon setection]("/Images/pigeon_found.png")
## Features:

- Real-time object detection using OpenCV and COCO model
- Triggered by an IR motion sensor for power/compute efficiency
- Activates a servo motor when a pigeon is detected
- Specifically monitors for birds among other COCO-classified objects
- Runs on a Raspberry Pi (tested on Raspberry Pi 4)

## Hardware

- Raspberry Pi 3/4/5 (or compatible model), 4+ is ideal
- Pi Camera module
- PIR (Passive Infrared) motion sensor
- Servo motor
- LEDs to act as signal lights
- Jumper wires, resistors (220 ohms) and a breadboard
- Power supply (5V for Raspberry Pi and components)
- some enclosure, either plastic cases or cardboard to encapsulate devices

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
