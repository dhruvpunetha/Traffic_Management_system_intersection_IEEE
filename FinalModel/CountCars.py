import cv2           #for using computer vision to take images
import numpy as np   #numerical python library to work with various datastructures and arrays

                     # count is a function that is counting cars from a image

def count():
    
    # Loading Yolo
    
    net = cv2.dnn.readNet("D:\CODING\Trafficmanagement\myYOLOMODEL\yolov3.weights", "D:\CODING\Trafficmanagement\myYOLOMODEL\yolov3.cfg") #specify the path for weight and cfg file
    classes = []                                                                   #for stroing various things yolo can detect

    with open("D:\CODING\Trafficmanagement\myYOLOMODEL\coco.names", "r") as namef: #extracting name of various oject yolo can detect from its coco.name file
        classes = [line.strip() for line in namef.readlines()]                     #classes is storing all the various classes yolo can detect
    
    layer_names = net.getLayerNames()                     #It gives you list of all layers used in a network. yolo v3 has 250
    
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    cp=cv2.VideoCapture(0)                                #capturing the video using camera to take pictures
    
    imnum=1                                               #image number that we are about to take we are storing the number of images


    ret, img = cp.read()                                  #"Frame" will get the next frame in the camera while "Ret" will obtain return value from getting the camera frame, either true of false.

    cv2.imwrite('D:\CODING\Trafficmanagement\carcounterimage\clicked'+str(imnum)+'.png', img) #storing this image

    img = cv2.imread('D:\CODING\Trafficmanagement\carcounterimage\clicked'+str(imnum)+'.png') #using this image
    imnum=imnum+1                                         #incrementing this so next image will be called clicked n+1
    
    img = cv2.resize(img, None, fx=0.4, fy=0.4)           #resizing image as per our use
    height, width, channels = img.shape
    # Detecting objects

    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False) #returns a blob converted by yolo
    net.setInput(blob)                                    #Sets the new input value for the network.

    outs = net.forward(output_layers)                     #compute output of layer with name

    car,bicycle,vehicle,bus,motorbike,truck=0,0,0,0,0,0   #keeping counts of various vehicles
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:              # finding detections from the scores
            scores = detection[5:]         #seeing the score for detection for all classes that yolo cand etect
            
            class_id = np.argmax(scores)    #the one with max score is what we think is the best prediction for the detection
            confidence = scores[class_id]   #storing the max confidence among the detections

            if confidence > 0.5:            #if the confidence on the class id is more then 50 percent we take it as a valid detection
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])                  #appending coordinates to boxes 
                confidences.append(float(confidence))       #appending confidence of object to confidences 
                class_ids.append(class_id)                  #appending class id of object detected to class_ids 
                
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):                             #counting number of cars/trucks/bicycle etc in our image
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])              #checking label of the class in classes
           
            if(label=="car"):                               #if car car count increase
                car+=1
                vehicle+=1
            if(label=="truck"):                             #if truck truck count increase
                truck+=1
                vehicle+=1
            if(label=="bicycle"):                           #if bicycle bicycle count increase
                bicycle+=1
                vehicle+=1
            if(label=="bus"):                               #if bus bus count increase
                bus+=1
                vehicle+=1
            if(label=="motorbike"):                         #if motorbike motorbike count increase
                bus+=1
                vehicle+=1

    return (car,bicycle,bus,motorbike,truck,vehicle)
