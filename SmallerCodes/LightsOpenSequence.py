import cv2
import time
import numpy as np
import work as w
import os
#print(w.count())
def dete(insec):
    car,bicycle,bus,motorbike,truck,vehicle=w.count()
    print(car,truck,bicycle,bus,motorbike)
    carw,bicyclew=5,5             #Adding Weights for each vehicle type
    truckw=8
    busw=10
    motorbikew=4
    li=[car,truck,bicycle,bus,motorbike]
    li1=[carw,truckw,bicyclew,busw,motorbikew]
    os.system('cls')
    print("Total Vehicle Detected at intersection ",insec," are: ",vehicle)
    timer=5 #even if no vehicle detected a minimum time is given
    for i in range(len(li)):
        if i==0 or i==2 or i==4:                    #Setting timer for green Light
           if(li[i]!=0):
                timer+=li[i]*li1[i]
                timer//=1.5
        else:
            if(li[i]!=0):
                timer+=li[i]*li1[i]
    timer=int(timer)
    return timer
def greensig(timer,ind):
    while timer>0:
        mins,secs=divmod(timer,60)
        t='{:02d}:{:02d}'.format(mins,secs)         
        print("WE ARE AT INTERSECTION ",ind,"GREEN LIGHT WILL BE ON TILL ",t,end='\r')
        time.sleep(1)                                           #Timer Countdown
        timer-=1
    os.system('cls')
def main():
    while(True):
        intersec=[1,2,3,4]
        for i in intersec:
            greensig(dete(i),i)
        ch=input("PRESS 1 to continue")
        if(ch!='1'):
            break
if __name__=="__main__":
    main()