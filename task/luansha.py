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
cap_l = cv2.VideoCapture(r"http://169.254.121.50:8080/?action=stream")
cap_r = cv2.VideoCapture(r"http://169.254.3.16:8080/?action=stream")

# region 模块化算法
def angleCal(x,y):
    if x!=0 and y!=0 and x!=y:
        return math.atan(x/y)*180/math.pi
def imgRoundDect(img):
    ret, thre_img1 = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
    return 255 - thre_img1



def drawCenterPoint(img,imgName):
    meanX, meanY = centerPoint(img)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.circle(img_rgb, (meanX, meanY), 3, (0, 0, 255))
    cv2.imshow("centerPoint"+str(imgName), img_rgb)
    return meanX, meanY


def drawCont(thimg):
    tempimg = thimg.copy()
    contours = findRealCont(tempimg)
    img_rgb = cv2.cvtColor(tempimg, cv2.COLOR_GRAY2BGR)
    for point in contours:
        cv2.circle(tempimg, point, 1, (0, 0, 255))
    cv2.imshow("Cont", tempimg)


def drawPointonImg(img, px, py):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.circle(img_rgb, (px, py), 3, (0, 0, 255))
    cv2.imshow("centerPoint", img_rgb)

# endregion

# region 控制变量
isFirstShow = True
LastX_l = 0
LastX_r = 0
DireX_l = 0
DireX_r = 0
LastY_l = 0
LastY_r = 0
DireY_l = 0
DireY_r = 0
Ttime = []
startTime = time.time()
LastTime = startTime
# endregion
Lresult = 0

# 首先要看看应该用哪个
frameCounter=0

l_XMIN = float("inf")
l_XMAX = -l_XMIN
r_XMIN = float("inf")
r_XMAX = -r_XMIN

while True:
    if time.time() - ProgramStartTime > 23:
        break
    # region 取帧
    ret, frame_l = cap_l.read()
    ret, frame_r = cap_r.read()
    frameCounter = frameCounter + 1

    thimg_l = imgRoundDect(cv2.cvtColor(frame_l, cv2.COLOR_BGR2GRAY))  # 二值化
    thimg_r = imgRoundDect(cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY))  # 二值化
    X_l, Y = drawCenterPoint(thimg_l,"thimg_l")
    X_r, Y = drawCenterPoint(thimg_r,"thimg_r")

    # l_XMIN = min(l_XMIN, X_l)
    # l_XMAX = max(l_XMAX, X_l)
    # r_XMIN = min(r_XMIN, X_r)
    # r_XMAX = max(r_XMAX, X_r)
    # print(f"L:{l_XMAX-l_XMIN} R:{r_XMAX-r_XMIN}")
    # print(f"Angle is {angleCal(l_XMAX - l_XMIN, r_XMAX - r_XMIN)}")


    # region 往复判断
    if LastX_l == 0:
        LastX_l = X_l
        DireX = signal(X_l - LastX_l)
    if LastX_r == 0:
        LastX_r = X_r
        DireX = signal(X_r - LastX_r)

    # is Left Reversed
    if (X_l - LastX_l) * DireX_l < 0 and time.time() - LastTime > 0.5:
        DireX_l = -DireX_l
        Ttime.append(time.time() - LastTime)
        LastTime = time.time()
        print(f"T is {Ttime[-1]}")
        Lresult = Time2Length(2 * np.mean(Ttime)) * 100
        print(f"L is {Lresult} cm")
    if (X_r - LastX_r) * DireX_r < 0 and time.time() - LastTime > 0.5:
        couter = couter + 1
        DireX_r = -DireX_r
        DireY = -DireY
        if couter == 5:
            startTime = time.time()
            LastTime = startTime
        if couter > 5:
            Ttime.append(time.time() - LastTime)
            LastTime = time.time()
            print(f"T is {Ttime[-1]}")
            Lresult = Time2Length(2 * np.mean(Ttime)) * 100
            print(f"L is {Lresult} cm")
    LastX = X
    LastY = Y
    # endreigon
    # region 按Esc键退出
    k = cv2.waitKey(1)
    if k == 27:
        break
    # endregion

cap_l.release()
cap_r.release()
cv2.destroyAllWindows()
print(f"Final Angle is {angleCal(l_XMAX-l_XMIN,r_XMAX-r_XMIN)}")

#=====Send Result to Terminal=====
