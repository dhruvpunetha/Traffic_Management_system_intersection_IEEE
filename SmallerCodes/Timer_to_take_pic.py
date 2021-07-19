
import cv2
import time
# SET THE COUNTDOWN TIMER
TIMER = int(5)
# Open the camera
cap = cv2.VideoCapture(0)
while True:
     
  
    ret, img = cap.read()
    cv2.imshow('a', img)
 
    # check for the key pressed
    k = cv2.waitKey(125)
 
    # set the key for the countdown
    # to begin. Here we set q
    if k == ord('q'):
        prev = time.time()
 
        while TIMER >= 0:
            ret, img = cap.read()
 
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, str(TIMER),
                        (200, 250), font,
                        7, (0, 255, 255),
                        4, cv2.LINE_AA)
            cv2.imshow('a', img)
            cv2.waitKey(125)
 
            cur = time.time()

            if cur-prev >= 1:
                prev = cur
                TIMER = TIMER-1
 
        else:
            ret, img = cap.read()

            cv2.imshow('a', img)

            cv2.waitKey(2000)
            ii=2

            cv2.imwrite('camera'+str(ii)+'.jpg', img)

    # Press Esc to exit
    elif k == 27:
        break
 
# close the camera
cap.release()
  
# close all the opened windows
cv2.destroyAllWindows()