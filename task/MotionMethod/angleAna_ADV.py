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
    contours = findRealCont(thimg)
    tempimg = cv2.cvtColor(thimg, cv2.COLOR_GRAY2BGR)
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
LastX_l = -1
LastX_r = -1
DireX_l = 0
DireX_r = 0
DireY_l = 0
DireY_r = 0
Ttime = []
startTime = time.time()
LastTime = startTime
# endregion
Lresult = 0


# l_XMIN = float("inf")
# l_XMAX = -l_XMIN
# r_XMIN = float("inf")
# r_XMAX = -r_XMIN

Lupdated=False
Rupdated=False
LastHighX_l=0
LastHighX_r=0
Xrange_l=0
Xrange_r=0


while True:
    if time.time() - ProgramStartTime > 23:
        break
    # region 取帧
    ret, frame_l = cap_l.read()
    ret, frame_r = cap_r.read()

    thimg_l = imgRoundDect(cv2.cvtColor(frame_l, cv2.COLOR_BGR2GRAY))  # 二值化
    thimg_r = imgRoundDect(cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY))  # 二值化
    X_l, Y = drawCenterPoint(thimg_l,"thimg_l")
    X_r, Y = drawCenterPoint(thimg_r,"thimg_r")


    # region 往复判断
    if LastX_l == -1:
        LastX_l = X_l
        DireX_l = 1
        LastHighX_l=X_l
    if LastX_r == -1:
        LastX_r = X_r
        DireX_r = 1
        LastHighX_r = X_r
    # is Left Reversed
    # print((X_l - LastX_l) * DireX_l)
    if (X_l - LastX_l) * DireX_l < 0 :
        Lupdated=True
        DireX_l = -DireX_l
        Xrange_l=abs(LastHighX_l-X_l)
        LastHighX_l=X_l

    if (X_r - LastX_r) * DireX_r < 0 :
        Rupdated = True
        DireX_r = -DireX_r
        Xrange_r = abs(LastHighX_r - X_r)
        LastHighX_r=X_r

    LastX_l = X_l
    LastX_r = X_r
    if Lupdated and Rupdated:
        Lupdated=False
        Rupdated=False
        print(f"Angle is {angleCal(Xrange_l,Xrange_r)}")

    # endreigon
    # region Esc close all windows
    k = cv2.waitKey(1)
    if k == 27:
        break
    # endregion

cap_l.release()
cap_r.release()
cv2.destroyAllWindows()
print(f"Final Angle is {angleCal(Xrange_l,Xrange_r)}")
