import cv2
import time
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
cp=cv2.VideoCapture(0) #capturing the video using camera to take pictures
imnum=10 #image number that we are about to take
while True:
    ret, img = cp.read()
    cv2.imshow('image show', img)
    k = cv2.waitKey(1) #wait key specifies the wait time before next frame
    # set the key for the countdown
    Timer = int(2)  #our timer in hich we take the next image
    if k == ord('q'):
        prev = time.time()
        while Timer >= 0:
            ret, img = cp.read()
            font = cv2.FONT_ITALIC
            cv2.putText(img, str(Timer),(50, 50), font,2, (0, 144, 170))
            cv2.imshow('image show', img) #show current image
            cv2.waitKey(1)
            cur = time.time() #current time
            if (cur-prev >= 1):
                prev = cur
                Timer = Timer-1
    
        ret, img = cp.read()
        cv2.imshow('clicked image', img)
        cv2.waitKey(2000)
        cv2.imwrite('Traffic_Management_system_intersection_IEEE\SmallerCodes\clicked'+str(imnum)+'.png', img)
        im = cv2.imread('Traffic_Management_system_intersection_IEEE\SmallerCodes\clicked'+str(imnum)+'.png')
        imnum=imnum+1
        
        bbox, label, conf = cv.detect_common_objects(im)
        output_image = draw_bbox(im, bbox, label, conf)
        plt.imshow(output_image)
        plt.show()
        #print('Number of cars in the image is '+ str(label.count('car')))
    elif(k==27):
        break
# close the camera
cp.release()
  
# close all the opened windows
cv2.destroyAllWindows()
