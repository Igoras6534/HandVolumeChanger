import cv2 
import time
import hand_tracking_modoule as htm
import numpy as np
import math



from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange=volume.GetVolumeRange()
minvol=volRange[0]
maxvol=volRange[1]


ptime=0
cam=cv2.VideoCapture(1)
detector=htm.handDetector(maxHands=1,detectionCon=0.7)

## Camera 
wCam,hCam=640,480
cam.set(3,wCam)
cam.set(4,hCam)

volbar=100
volper=0
while True:
    success,img=cam.read()
    frame=cv2.flip(img,1)
    frame=detector.findHands(frame,draw=False)
    lmList=detector.findPosition(frame,draw=False)
    cv2.rectangle(frame,(100,400),(540,430),(255,0,0),2)
    if len(lmList)!=0:
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]     
        cx,cy=(x1+x2)//2,(y1+y2)//2
    
        cv2.circle(frame,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(frame,(x2,y2),10,(255,0,255),cv2.FILLED)
        cv2.circle(frame,(cx,cy),6,(255,0,255),cv2.FILLED)
        cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)

        lenght=math.hypot(x2-x1,y2-y1)
        #Range 18-190
        #Volume range -65-0
        vol=np.interp(lenght,[20,190],[minvol,maxvol])
        volbar=np.interp(lenght,[20,190],[100,540])
        volper=np.interp(lenght,[20,190],[0,100])


        volume.SetMasterVolumeLevel(vol, None)
        cv2.rectangle(frame,(100,400),(int(volbar),430),(255,0,0),cv2.FILLED)

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime


    
    cv2.putText(frame,f"FPS:{(int(fps))}", (40,70), cv2.FONT_HERSHEY_PLAIN, 2,  
    (255,0,0),2)
    cv2.putText(frame,f"{(int(volper))}%", (310,390), cv2.FONT_HERSHEY_PLAIN, 2,  
    (255,0,0),2)

    cv2.imshow("Image",frame)
    
    if cv2.waitKey(1)==ord("q"):
        break
    