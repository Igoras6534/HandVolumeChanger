import cv2 
import mediapipe as mp
import time


class handDetector():
    def __init__(self,mode=False,maxHands=2, model_complexity=1,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        self. model_complexity=model_complexity
        
        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxHands,self.model_complexity, 
                                      self.detectionCon,self.trackCon)
        self.mpDraw=mp.solutions.drawing_utils
        print("Initialized")


    def findHands(self,frame,draw=True):       
        frameRGB=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(frameRGB)
        if self.results.multi_hand_landmarks:
            for hand_LMS in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame,hand_LMS,
                                               self.mpHands.HAND_CONNECTIONS)
        return frame
    def findPosition(self, frame, handNo=0, draw=True):
        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h,w,c=frame.shape
                cx,cy=int(lm.x * w),int(lm.y*h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(frame,(cx,cy),6,(255,0,255),cv2.FILLED) 
        return lmList
                



def main():
    ptime=0
    ctime=0
    cam=cv2.VideoCapture(1)
    detector=handDetector()
    while True:
        success,frame=cam.read()
        frame=detector.findHands(frame)
        lmList=detector.findPosition(frame,)

            





        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime
    
        cv2.putText(frame,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3,  
        (255,0,255),3)
        cv2.imshow("Image",frame)
        
        if cv2.waitKey(1)==ord("q"):
            break
        

if __name__=="__main__":
    
    main()

