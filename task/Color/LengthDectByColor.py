#使用BackgroundSubtractorMOG
import cv2 as cv
import numpy as np
from task.myopencvTool import *

ProgramStartTime=time.time()
cam=CamerSystem()


CenterXCor=0
CenterXCors=[]

LastX=-1
LastDirection=-2
Ttime=[]
while True:
    X=cam.GetCenterByColor()[0]
    # print((X-CenterXCor))
    if X==-1:
        continue
    if LastX==-1:
        LastX=X
        continue
    if LastDirection==-2:
        LastDirection=signal(X-LastX)
        continue
    # Direction=signal(X-LastX)
    # print(Direction)
    if X-LastX==0:
        continue
    if abs(X-CenterXCor)<5 and time.time()-LastTime>0.7:
        Ttime.append(time.time()-LastTime)
        LastTime = time.time()
        LastDirection=-LastDirection
        print("T is ")
        print(Ttime[-1])
        print("L is ")
        print(Time2Length(2 * Ttime[-1]) * 100)
    # cv.imshow("draw", draw1)
    LastX=X
    k = cv.waitKey(1)
    if k == 27:
        break
print("FInal L is ")

print(Time2Length(2*np.nanmean(Ttime[2:-2]))*100-7.5)
cap.release()
cv.destroyAllWindows()