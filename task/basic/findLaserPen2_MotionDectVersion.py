#使用BackgroundSubtractorMOG
import cv2 as cv
import numpy as np
from task.myopencvTool import *


# 设置文件
file_test = r"http://169.254.121.50:8080/?action=stream"

cap = cv.VideoCapture(file_test)

# 设置变量
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (2, 2))  # 定义结构元素
color_m = (0, 0, 255)

# 背景差法
# fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
# fgbg=cv.createBackgroundSubtractorMOG2(detectShadows=False,varThreshold=20)
fgbg =cv.createBackgroundSubtractorKNN()


Lx=0
Ly=0
Lw=0
Lh=0
while True:
    # 读取一帧
    ret, frame = cap.read()
    # 如果视频结束，跳出循环
    if not ret:
        break
    # frame = cv.resize(frame, (500, 500), interpolation=cv.INTER_CUBIC)
    frame_motion = frame.copy()
    cv.imshow("source", frame_motion)

    # 计算前景掩码
    fgmask = fgbg.apply(frame_motion)
    # cv.imshow("MaskMOG",fgmask )
    drawCenterPoint(fgmask,"CenterOfMask")




    # draw1 = cv.threshold(fgmask, 100, 255, cv.THRESH_BINARY)[1]  # 二值化
    # cv.imshow("Thre",draw1 )
    draw1=open_mor(fgmask,3,1)
    draw1 = cv.dilate(draw1, kernel, iterations=3)
    cv.imshow("OPENED",draw1)

    # 查找检测物体的轮廓,只检测外轮廓,只需4个点来保存轮廓信息
    contours_m, hierarchy_m = cv.findContours(fgmask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    NoSat=True
    for c in contours_m:
        print(cv.contourArea(c))
        if cv.contourArea(c) < 1000:
            continue
        NoSat=False
        (Lx,Ly,Lw,Lh)=(x, y, w, h) = cv.boundingRect(c)
        cv.rectangle(frame_motion, (x, y), (x + w, y + h), color_m, 2)
    if NoSat:
        cv.rectangle(frame_motion, (Lx, Ly), (Lx + Lw, Ly + Lh), color_m, 2)
    cv.imshow("apply", frame_motion)
    k = cv.waitKey(1)
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()