import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import math
import sys
from myopencvTool import *
# sys.path.append("..")

from task.myopencvTool import *

ProgramStartTime = time.time()

ObjectLength=7.5

# 620x480
cap_l = cv2.VideoCapture(r"http://169.254.121.50:8080/?action=stream")
cap_r = cv2.VideoCapture(r"http://169.254.3.16:8080/?action=stream")
# region 控制变量
isFirstShow = True
LastX_l = -1
LastX_r = -1
DireX_l = 1
DireX_r = 1
DireY_l = 0
DireY_r = 0
Ttime_l = []
Ttime_r = []
startTime = time.time()
# LastTime_l = startTime
# LastTime_r = startTime
# endregion
Lresult_l = 0
Lresult_r = 0


Lupdated=False
Rupdated=False
LastHighX_l=0
LastHighX_r=0
Xrange_l=0
Xrange_r=0

l_XMIN = 0
l_XMAX = 0
r_XMIN = 0
r_XMAX = 0

framesReadCounter_l=0
framesReadCounter_r=0
FPS=30
while True:
    #timer Break
    if time.time() - ProgramStartTime > 15:
        break
    # region Take image and basic Process
    ret, frame_l = cap_l.read()
    ret, frame_r = cap_r.read()
    framesReadCounter_l=framesReadCounter_l+1
    framesReadCounter_r=framesReadCounter_r+1

    thimg_l = imgThresholdCust(cv2.cvtColor(frame_l, cv2.COLOR_BGR2GRAY),80)  # 二值化
    thimg_r = imgThresholdCust(cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY),80)  # 二值化

    showimgInPanel(thimg_l)

    X_l, Y = drawCenterPoint(thimg_l,"thimg_l")
    X_r, Y = drawCenterPoint(thimg_r,"thimg_r")

    l_XMIN = min(l_XMIN, X_l)
    l_XMAX = max(l_XMAX, X_l)
    r_XMIN = min(r_XMIN, X_r)
    r_XMAX = max(r_XMAX, X_r)
    # Initialize the first Value
    if LastX_l == -1:
        LastX_l = X_l
        LastHighX_l=X_l
    if LastX_r == -1:
        LastX_r = X_r
        LastHighX_r = X_r

    # region GoBackDect

    # is Left Reversed
    if (X_l - LastX_l) * DireX_l < -1 and framesReadCounter_l > 25:
        DireX_l = -DireX_l

        #Length Calculate Data
        Ttime_l.append(framesReadCounter_l*(1.0/FPS))
        framesReadCounter_l=0
        print(f"T is {Ttime_l[-1]}")
        Lresult_l = Time2Length(2 * Ttime_l[-1]) * 100
        print(f"L1 is {Lresult_l} cm")

        #Angle Analys Data
        Lupdated=True
        Xrange_l=abs(LastHighX_l-X_l)
        LastHighX_l=X_l
    if (X_r - LastX_r) * DireX_r < -1 and framesReadCounter_r > 25:
        DireX_r = -DireX_r

        # Length Calculate Data
        Ttime_r.append(framesReadCounter_r*(1.0/FPS))
        framesReadCounter_r=0
        LastTime_r = time.time()
        # print(f"T is {Ttime[-1]}")
        # Lresult_r= Time2Length(2 * np.mean(Ttime_r)) * 100
        # print(f"L2 is {Lresult_r} cm")

        # Angle Analys Data
        Rupdated = True
        Xrange_r = abs(LastHighX_r - X_r)
        LastHighX_r = X_r
    if Lupdated and Rupdated:
        Lupdated = False
        Rupdated = False
        print(f"Angle is {angleCal(Xrange_l, Xrange_r)}")

    LastX_l = X_l
    LastX_r = X_r
    # endreigon
    # region 按Esc键退出
    k = cv2.waitKey(1)
    if k == 27:
        break
    # endregion

camera.releasCam()
cv2.destroyAllWindows()
Lresult_l = Time2Length(2 * np.mean(Ttime_l[1:])) * 100
Lresult_r = Time2Length(2 * np.mean(Ttime_r[1:])) * 100

# if (l_XMAX-l_XMIN)>(r_XMAX-r_XMIN):
print(f"真实摆长:{Lresult_l}cm,摆线长度:{Lresult_l - ObjectLength}cm")
# else:
print(f"真实摆长:{Lresult_r}cm,摆线长度:{Lresult_r - ObjectLength}cm")

print(f"Final Angle is {angleCal(Xrange_l,Xrange_r)}")

