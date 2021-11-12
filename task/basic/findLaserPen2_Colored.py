#使用BackgroundSubtractorMOG
import cv2 as cv
import numpy as np
from task.myopencvTool import *

def open_mor(src,kernelsize,iter):
    kernel = np.ones((kernelsize,kernelsize),np.uint8)
    opening = cv.morphologyEx(src,cv.MORPH_OPEN,kernel, iterations=iter) #iterations进行3次操作
    # cv.imshow('open',opening)
    return opening
def close_mor(src,kernelsize,iter):
    kernel = np.ones((kernelsize,kernelsize),np.uint8)
    opening = cv.morphologyEx(src,cv.MORPH_CLOSE,kernel, iterations=iter) #iterations进行3次操作
    # cv.imshow('open',opening)
    return opening
# 设置文件
file_test = r"http://192.168.0.120:8080/?action=stream"

cap = cv.VideoCapture(file_test)

# 设置变量
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (2, 2))  # 定义结构元素
color_m = (0, 0, 255)

# 背景差法
# fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
# fgbg=cv.createBackgroundSubtractorMOG2(detectShadows=False,varThreshold=20)
# fgbg =cv.createBackgroundSubtractorKNN()

lower_red = np.array([25,20,70])
upper_red = np.array([60,50,100])
# 113, 12, 42
while True:
    # 读取一帧
    ret, frame = cap.read()
    # frame = cv.resize(frame, (500, 500), interpolation=cv.INTER_CUBIC)
    frame_motion = frame.copy()
    cv.imshow("source", frame_motion)


    color_fliter=cv.inRange(frame_motion,lower_red,upper_red)
    # cv.imshow("Color",color_fliter)
    drawCenterPoint(color_fliter.copy(),"Color")

    # openedMask = open_mor(color_fliter, 3, 1)
    # # print(cv.moments(closedMask)["m00"])
    # drawCenterPoint(openedMask, "CenterOfMog")
    #
    # closedMask=close_mor(openedMask,30,5)
    # # print(cv.moments(closedMask)["m00"])
    # drawCenterPoint(closedMask,"CenterOfMog2")
    closedMask=color_fliter



    draw1 = cv.dilate(closedMask, kernel, iterations=1)

    # 查找检测物体的轮廓,只检测外轮廓,只需4个点来保存轮廓信息
    contours_m, hierarchy_m = cv.findContours(closedMask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for c in contours_m:
        print(cv.contourArea(c))
        if cv.contourArea(c) < 1000:
            continue
        (x, y, w, h) = cv.boundingRect(c)
        cv.rectangle(frame_motion, (x-10, y-10), (x + w, y + h), color_m, 2)

    cv.imshow("apply", frame_motion)
    cv.imshow("draw", draw1)
    k = cv.waitKey(1)
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()