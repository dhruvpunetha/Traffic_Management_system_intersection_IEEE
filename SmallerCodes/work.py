import cv2
import time
import numpy as np
def count():
    # Load Yolo
    net = cv2.dnn.readNet("D:\CODING\Trafficmanagement\myYOLOMODEL\yolov3.weights", "D:\CODING\Trafficmanagement\myYOLOMODEL\yolov3.cfg") #specify the path for weight and cfg file
    classes = [] #for stroing various things yolo can detect
    with open("D:\CODING\Trafficmanagement\myYOLOMODEL\coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]   #classes is storing all the various classes yolo can detect
    layer_names = net.getLayerNames()  #It gives you list of all layers used in a network. yolo v3 has 250
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    #colors = np.random.uniform(0, 255, size=(len(classes), 3))
    cp=cv2.VideoCapture(0) #capturing the video using camera to take pictures
    imnum=1 #image number that we are about to take we are storing the number of images
    #Timer = int(2)  #our timer in which we take the next image
    #prev = time.time() #to take starting time  with which we know how much time passed
    '''while Timer >= 0:
        cur = time.time() #current time so we can see if 1 sec has passed
        if (cur-prev >= 1): #checking if 1 sec has passed or not
            prev = cur
            Timer = Timer-1'''
    ret, img = cp.read() # #"Frame" will get the next frame in the camera while "Ret" will obtain return value from getting the camera frame, either true of false.
    cv2.imwrite('D:\CODING\Trafficmanagement\SmallerCodes\clicked'+str(imnum)+'.png', img) #storing this image
    img = cv2.imread('D:\CODING\Trafficmanagement\SmallerCodes\clicked'+str(imnum)+'.png') #using this image
    imnum=imnum+1
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape
    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False) #blob converted by yolo
    net.setInput(blob)
    outs = net.forward(output_layers)
    car,bicycle,vehicle,bus,motorbike,truck=0,0,0,0,0,0   #keeping counts of various vehicles
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)   #the one with max score is what we think is the best prediction for the detection
            confidence = scores[class_id]
            if confidence > 0.5:   #if the confidence on the class id is more then 50 percent we take it as a valid detection
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h]) #appending coordinates to boxes 
                confidences.append(float(confidence)) #appending confidence of object to confidences 
                class_ids.append(class_id) #appending class id of object detected to class_ids 
                
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):   #counting number of cars/trucks/bicycle etc in our image
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            if(label=="car"):
                car+=1
                vehicle+=1
            if(label=="truck"):
                truck+=1
                vehicle+=1
            if(label=="bicycle"):
                bicycle+=1
                vehicle+=1
            if(label=="bus"):
                bus+=1
                vehicle+=1
            if(label=="motorbike"):
                bus+=1
                vehicle+=1
            #color = colors[class_ids[i]]
    return (car,bicycle,bus,motorbike,truck,vehicle)
