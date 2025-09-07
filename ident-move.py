import cv2
from picamera2 import Picamera2
import os
import time
from gpiozero import AngularServo
import subprocess

#servo = AngularServo(18, initial_angle=0, min_pulse_width=0.0006, max_pulse_width=0.0023)

# === Setup paths ===
current_path = os.getcwd()
class_file = os.path.join(current_path, "models/coco.names")
config_file = os.path.join(current_path, "models/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
weights_file = os.path.join(current_path, "models/frozen_inference_graph.pb")


classNames = []
with open(class_file,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

net = cv2.dnn_DetectionModel(weights_file,config_file)
#net.setInputSize(320,320)
net.setInputSize(160,160) # or 224

net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img, thres, nms, draw=False, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    return img,objectInfo

# === Main camera loop ===
if __name__ == "__main__":

    # Picam codr
    picam2 = Picamera2()
    
    #picam2.preview_configuration.main.size = (800,800)
    #picam2.preview_configuration.main.format = "RGB888"
    #picam2.preview_configuration.align()

    # Use a smaller resolution for speed, adjust as needed
    picam2.preview_configuration.main.size = (640, 480)
    picam2.preview_configuration.main.format = "YUV420"
    #picam2.preview_configuration.align()

    picam2.configure("preview")
    picam2.start()
    time.sleep(0.1) # warm up camera

    frames = 0
    while frames < 20:

        # Picam campture in RGB
        #img = picam2.capture_array()
        # Or capture in YUV format
        img = picam2.capture_array("main")
        
        # Convert YUV to BGR for OpenCV display
        img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR_I420)
        
        # Pass image to object detection
        #img = cv2.resize(img, (400,400))
        #result_img, objectInfo = getObjects(img, 0.45, 0.2, objects=['bird']) 
        result_img, objectInfo = getObjects(img, 0.20, 0.2, objects=['bird'])
        
        cv2.imshow("Output",result_img)

        print("objects detected:", objectInfo, "frames so far", frames) # which object in the object set, other info
        frames = frames + 1

        if cv2.waitKey(1) == ord('q'):
            break
        if len(objectInfo) != 0:
            #print('actiavting servo')
            #subprocess.run(['python', 'servo_smooth_func.py'])
            subprocess.run(['python', 'rotate_180.py'])

    cv2.destroyAllWindows()

