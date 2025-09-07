import cv2
from picamera2 import Picamera2
from libcamera import Transform
import os
import time


# === Setup paths ===
current_path = os.getcwd()
#print(current_path)
class_file = os.path.join(current_path, "models/coco.names")
config_file = os.path.join(current_path, "models/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
weights_file = os.path.join(current_path, "models/frozen_inference_graph.pb")


classNames = []
with open(class_file,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

net = cv2.dnn_DetectionModel(weights_file,config_file)
#net.setInputSize(320,320)
net.setInputSize(160,160)

net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img, thres, nms, draw=True, objects=[]):
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

    # Picam code
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (600,600) #width, height
    picam2.preview_configuration.main.format = "RGB888"

    #picam2.preview_configuration.main.format = "RGB565"

    picam2.preview_configuration.align()
    #picam2.preview_configuration.transform = Transform(rotation=90)
    picam2.configure("preview")
    picam2.start()
    time.sleep(0.1) # warm up camera

    # opencv code
    '''
    cap = cv2.VideoCapture(0) # doesnt work with pi 3
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)
    '''

    while True:
        
        # Picam code
        img = picam2.capture_array()
        result_img, objectInfo = getObjects(img, 0.50, 0.2, objects=['bird', 'person']) 

        #result_img, objectInfo = getObjects(img,0.45,0.2, objects=['bird', 'person']) 
        #result_img, objectInfo = getObjects(img,0.45,0.2)


        print(objectInfo)
        #rot_img = cv2.rotate(result_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imshow("Output",result_img)
        if cv2.waitKey(1) == ord('q'):
            break

        # opencv code
        '''
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.45,0.2)
        #print(objectInfo)
        cv2.imshow("Output",img)
        cv2.waitKey(1)
        '''
    cv2.destroyAllWindows()

