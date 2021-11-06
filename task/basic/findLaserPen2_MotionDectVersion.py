#使用BackgroundSubtractorMOG
import cv2 as cv
import numpy as np

def open_mor(src,kernelsize,iter):
    kernel = np.ones((kernelsize,kernelsize),np.uint8)
    opening = cv.morphologyEx(src,cv.MORPH_OPEN,kernel, iterations=iter) #iterations进行3次操作
    # cv.imshow('open',opening)
    return opening
# 设置文件
file_test = r"http://192.168.0.101:8080/?action=stream"

cap = cv.VideoCapture(file_test)

# 设置变量
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (2, 2))  # 定义结构元素
color_m = (0, 0, 255)

# 背景差法
fgbg = cv.bgsegm.createBackgroundSubtractorMOG()

while True:
    # 读取一帧
    ret, frame = cap.read()
    # 如果视频结束，跳出循环
    if not ret:
        break
    frame = cv.resize(frame, (500, 500), interpolation=cv.INTER_CUBIC)
    frame_motion = frame.copy()

    # 计算前景掩码
    fgmask = fgbg.apply(frame_motion)
    draw1 = cv.threshold(fgmask, 0, 255, cv.THRESH_OTSU)[1]  # 二值化
    draw1=open_mor(draw1,3,1)
    draw1 = cv.dilate(draw1, kernel, iterations=1)

    # 查找检测物体的轮廓,只检测外轮廓,只需4个点来保存轮廓信息
    contours_m, hierarchy_m = cv.findContours(draw1.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for c in contours_m:
        print(cv.contourArea(c))
        # if cv.contourArea(c) < 100:
        #     continue
        (x, y, w, h) = cv.boundingRect(c)
        cv.rectangle(frame_motion, (x, y), (x + w, y + h), color_m, 2)

    cv.imshow("source", frame_motion)
    # cv.imshow("apply", fgmask)
    # cv.imshow("draw", draw1)
    k = cv.waitKey(1)
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()