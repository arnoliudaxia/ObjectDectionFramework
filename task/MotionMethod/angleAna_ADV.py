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
isFirstShow = True
LastX_l = -1
LastX_r = -1
DireX_l = 1
DireX_r = 1
DireY_l = 0
DireY_r = 0
Ttime = []
# endregion
AngleData = []

# l_XMIN = float("inf")
# l_XMAX = -l_XMIN
# r_XMIN = float("inf")
# r_XMAX = -r_XMIN

Lupdated = False
Rupdated = False
LastHighX_l = 0
LastHighX_r = 0
Xrange_l = 0
Xrange_r = 0

framesReadCounter = 0
FPS = 45
camera = CamerSystem()
# input("Press Enter To Start")
while True:
    if time.time() - ProgramStartTime > 23:
        break
    # region 取帧

    thimg_l, thimg_r = camera.MotionThreshold()
    framesReadCounter = framesReadCounter + 1

    # thimg_l = imgRoundDect(cv2.cvtColor(frame_l, cv2.COLOR_BGR2GRAY))  # 二值化
    # thimg_r = imgRoundDect(cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY))  # 二值化
    X_l, Y = drawCenterPoint(thimg_l, "thimg_l")
    X_r, Y = drawCenterPoint(thimg_r, "thimg_r")

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