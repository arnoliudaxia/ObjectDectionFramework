import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import math
import sys
# sys.path.append("..")

from task.myopencvTool import *

ProgramStartTime = time.time()
# 620x480


# region 控制变量
UseColor=1
LastX_l = -1
LastX_r = -1
DireX_l = 1
DireX_r = 1
DireY_l = 0
DireY_r = 0
Ttime = []
# endregion
AngleData = []


Lupdated = False
Rupdated = False
LastHighX_l = 0
LastHighX_r = 0
Xrange_l = 0
Xrange_r = 0

camera = CamerSystem()
# input("Press Enter To Start")
def GetXY():

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))  # 定义结构元素
    color_m = (0, 0, 255)


    lower_red = np.array([25,15,60])
    upper_red = np.array([60,50,100])
    ret, frame_l = camera.cap_l.read()
    ret, frame_r = camera.cap_r.read()
    # frame = cv2.resize(frame, (500, 500), interpolation=cv2.INTER_CUBIC)
    frame_motion_l = frame_l.copy()
    frame_motion_r = frame_r.copy()
    # cv2.imshow("source", frame_motion)


    color_fliter_l=cv2.inRange(frame_motion_l,lower_red,upper_red)
    color_fliter_r=cv2.inRange(frame_motion_r,lower_red,upper_red)
    # cv2.imshow("Color",color_fliter)
    # drawCenterPoint(color_fliter.copy(),"Color")

    closedMask_l = close_mor(color_fliter_l, 50, 1)
    closedMask_r = close_mor(color_fliter_r, 50, 1)
    # drawCenterPoint(closedMask.copy(),"Closed")

    l,contours_m_l, hierarchy_m = cv2.findContours(closedMask_l, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    l,contours_m_r, hierarchy_m = cv2.findContours(closedMask_r, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    X1=-1
    X2=-1
    for c in contours_m_l:
        # print(cv2.contourArea(c))
        if cv2.contourArea(c) < 1000:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame_motion_l, (x, y), (x + w, y + h), color_m, 2)
        X1=round((2*x+w)/2)
    for c in contours_m_r:
        # print(cv2.contourArea(c))
        if cv2.contourArea(c) < 1000:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame_motion_r, (x, y), (x + w, y + h), color_m, 2)
        X2 = round((2 * x + w) / 2)
    return X1,X2
while True:
    if time.time() - ProgramStartTime > 23:
        break
    # region 取帧
    X_l=0
    X_r=0
    if UseColor!=1:
        thimg_l, thimg_r = camera.MotionThreshold()
        X_l, Y = drawCenterPoint(thimg_l, "thimg_l")
        X_r, Y = drawCenterPoint(thimg_r, "thimg_r")
    else:
        X_l,X_r=GetXY()
    # region 往复判断
    if LastX_l == -1:
        LastHighX_l = LastX_l = X_l
    if LastX_r == -1:
        LastHighX_r = LastX_r = X_r
    # is Left Reversed
    # print((X_l - LastX_l) * DireX_l)
    if (X_l - LastX_l) * DireX_l <= -1:
        Lupdated = True
        DireX_l = -DireX_l
        Xrange_l = abs(LastHighX_l - X_l)
        LastHighX_l = X_l

    if (X_r - LastX_r) * DireX_r <= -1:
        Rupdated = True
        DireX_r = -DireX_r
        Xrange_r = abs(LastHighX_r - X_r)
        LastHighX_r = X_r

    LastX_l = X_l
    LastX_r = X_r
    if Lupdated and Rupdated:
        Lupdated = False
        Rupdated = False
        print("Angle is ")
        print(angleCal(Xrange_l, Xrange_r))
        # print(f"Angle is {angleCal(Xrange_l, Xrange_r)}")
        if angleCal(Xrange_l, Xrange_r)!=None:
            resultr=angleCal(Xrange_l, Xrange_r)
            if Xrange_l>Xrange_r:
                AngleData.append(resultr)
            else:
                AngleData.append(90-resultr)


    # endreigon
    # region Esc close all windows
    k = cv2.waitKey(1)
    if k == 27:
        break
    # endregion

camera.releasCam()
cv2.destroyAllWindows()
print("Final Angle is ")
print(np.mean(AngleData[2:]))