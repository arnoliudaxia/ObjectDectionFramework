#使用BackgroundSubtractorMOG
import cv2 as cv
import numpy as np
from task.myopencvTool import *


UseColor=1
UseStandardCenter=0

ProgramStartTime=time.time()

cam=CamerSystem()
cap_l=cam.cap_l
cap_r=cam.cap_r
def GetXY():

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  # 定义结构元素
    color_m = (0, 0, 255)


    lower_red = np.array([25,15,60])
    upper_red = np.array([60,50,100])
    ret, frame_l = cap_l.read()
    ret, frame_r = cap_r.read()
    # frame = cv.resize(frame, (500, 500), interpolation=cv.INTER_CUBIC)
    frame_motion_l = frame_l.copy()
    frame_motion_r = frame_r.copy()
    # cv.imshow("source", frame_motion)


    color_fliter_l=cv.inRange(frame_motion_l,lower_red,upper_red)
    color_fliter_r=cv.inRange(frame_motion_r,lower_red,upper_red)
    # cv.imshow("Color",color_fliter)
    # drawCenterPoint(color_fliter.copy(),"Color")

    closedMask_l = close_mor(color_fliter_l, 50, 1)
    closedMask_r = close_mor(color_fliter_r, 50, 1)
    # drawCenterPoint(closedMask.copy(),"Closed")

    l,contours_m_l, hierarchy_m = cv.findContours(closedMask_l, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    l,contours_m_r, hierarchy_m = cv.findContours(closedMask_r, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    X1=-1
    X2=-1
    for c in contours_m_l:
        # print(cv.contourArea(c))
        if cv.contourArea(c) < 1000:
            continue
        (x, y, w, h) = cv.boundingRect(c)
        cv.rectangle(frame_motion_l, (x, y), (x + w, y + h), color_m, 2)
        X1=round((2*x+w)/2)
    for c in contours_m_r:
        # print(cv.contourArea(c))
        if cv.contourArea(c) < 1000:
            continue
        (x, y, w, h) = cv.boundingRect(c)
        cv.rectangle(frame_motion_r, (x, y), (x + w, y + h), color_m, 2)
        X2 = round((2 * x + w) / 2)
    return X1,X2
def GetXYOne(cap):

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))  # 定义结构元素
    color_m = (0, 0, 255)


    lower_red = np.array([25,15,60])
    upper_red = np.array([60,50,100])
    ret, frame_l = cap.read()
    # frame = cv.resize(frame, (500, 500), interpolation=cv.INTER_CUBIC)
    frame_motion_l = frame_l.copy()
    # cv.imshow("source", frame_motion)


    color_fliter_l=cv.inRange(frame_motion_l,lower_red,upper_red)
    # cv.imshow("Color",color_fliter)
    # drawCenterPoint(color_fliter.copy(),"Color")

    closedMask_l = close_mor(color_fliter_l, 50, 1)
    # drawCenterPoint(closedMask.copy(),"Closed")

    l,contours_m_l, hierarchy_m = cv.findContours(closedMask_l, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for c in contours_m_l:
        # print(cv.contourArea(c))
        if cv.contourArea(c) < 1000:
            continue
        (x, y, w, h) = cv.boundingRect(c)
        cv.rectangle(frame_motion_l, (x, y), (x + w, y + h), color_m, 2)
        X,Y=round((2*x+w)/2),round((2*y+h)/2)
        LastX=X
        # frame_motion=cv.circle(frame_motion,(X,Y),2,(0,0,255))
        # cv.imshow("HH",frame_motion)
        return X

        # print("X is "+str(X))
    return -1

CenterX1Cor=0
CenterX2Cor=0
CenterX1Cors=[]
CenterX2Cors=[]
if UseStandardCenter==0:
    while True:
        if UseColor==1:
            X1,X2=GetXY()
        else:
            X1,X2=cam.MotionThreshold()
        CenterX1Cors.append(X1)
        CenterX2Cors.append(X2)
        if time.time()-ProgramStartTime>3:
            break
    CenterX1Cor=np.nanmean(CenterX1Cors)
    CenterX2Cor=np.nanmean(CenterX2Cors)
else:
    CenterX1Cor=320
    CenterX2Cor=320
input("Center Point1 :"+str(CenterX1Cor))
input("Center Point2 :"+str(CenterX2Cor))
l_XMIN = float("inf")
l_XMAX = -l_XMIN
r_XMIN = float("inf")
r_XMAX = -r_XMIN
# 首先要看看应该用哪个
cap=0
ProgramStartTime=time.time()
while True:
    if time.time()-ProgramStartTime>4:
        if l_XMAX - l_XMIN > r_XMAX - r_XMIN:
            cap = 1
        else:
            cap = 2
        break

    X_l=0
    X_r=0
    if UseColor!=1:
        frame_l, frame_r = cam.MotionThreshold()
        X_l, Y = centerPoint(frame_l)
        X_r, Y = centerPoint(frame_r)
    else:
        X_l,X_r=GetXY()
    l_XMIN = min(l_XMIN, X_l)
    l_XMAX = max(l_XMAX, X_l)
    r_XMIN = min(r_XMIN, X_r)
    r_XMAX = max(r_XMAX, X_r)


LastX=-1
LastDirection=-2
Ttime=[]
LastTime=time.time()
ProgramStartTime=LastTime

CenterXCor=0
if cap==1:
    CenterXCor=CenterX1Cor
else:
    CenterXCor=CenterX2Cor
while True:
    if UseColor==1:
        if cap==1:
            X=GetXYOne(cam.cap_l)
        else:
            X=GetXYOne(cam.cap_r)
    else:
        X=cam.MotionThreshold_l()[cap-1]
    # print((X-CenterXCor))
    if time.time()-ProgramStartTime>20:
        break
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