import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import math
import sys
import socket

ProgramStartTime = time.time()
# 620x480
cap_l = cv2.VideoCapture(r"http://169.254.121.50:8080/?action=stream")
cap_r = cv2.VideoCapture(r"http://169.254.3.16:8080/?action=stream")
cap=-1

# region 模块化算法
def showimg(img):
    plt.imshow(img, "gray")
    plt.show()


def imgRoundDect(img):
    ret, thre_img1 = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
    return 255 - thre_img1


# 计算二值化图像中有数据图像的中心点
def findRealCont(thimg):
    contours, hierarchy = cv2.findContours(thimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    finalCon = contours[0]
    for con in contours:
        if cv2.contourArea(con) < 1000:
            continue
        else:
            finalCon = con
    finalCon.resize(finalCon.shape[0], 2)
    return finalCon, thimg


def meanPoint(thimg):
    contours = findRealCont(thimg)
    avr_x, avr_y = np.mean(contours, axis=0)
    return int(avr_x), int(avr_y)


def centerPoint(thimg):
    mom = cv2.moments(thimg)
    center_x = int(mom["m10"] / mom["m00"])
    center_y = int(mom["m01"] / mom["m00"])
    return center_x, center_y


def drawCenterPoint(img):
    meanX, meanY = centerPoint(img)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.circle(img_rgb, (meanX, meanY), 3, (0, 0, 255))
    cv2.imshow("centerPoint", img_rgb)
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


def signal(intput):
    if intput >= 0:
        return 1
    if intput < 0:
        return -1


def Time2Length(time):
    return time ** 2 * 9.886 / (4 * math.pi ** 2)


# endregion

# region 控制变量
isFirstShow = True
LastX = 0
DireX = 0
LastY = 0
DireY = 0
Ttime = []
couter = 0
startTime = 0
LastTime = 0
# endregion
Lresult = 0

# 首先要看看应该用哪个
frameCounter=0

l_XMIN = float("inf")
l_XMAX = -l_XMIN
r_XMIN = float("inf")
r_XMAX = -r_XMIN
while True:
    if frameCounter>5:
        if l_XMAX-l_XMIN>r_XMAX-r_XMIN:
            cap=cap_l
        else:
            cap=cap_r
        break

    RangeXChangement=0

    ret, frame_l = cap_l.read()
    ret, frame_r = cap_r.read()
    frameCounter=frameCounter+1

    thimg_l = imgRoundDect(cv2.cvtColor(frame_l, cv2.COLOR_BGR2GRAY))  # 二值化
    thimg_r = imgRoundDect(cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY))  # 二值化
    X_l, Y = drawCenterPoint(thimg_l)
    X_r, Y = drawCenterPoint(thimg_r)

    l_XMIN = min(l_XMIN,X_l)
    l_XMAX = max(l_XMAX,X_l)
    r_XMIN =min(r_XMIN,X_r)
    r_XMAX =max(r_XMAX,X_r)

while True:
    if time.time() - ProgramStartTime > 23:
        break
    # region 取帧
    ret, frame = cap.read()
    # 如果视频结束，跳出循环
    if not ret:
        break
    cv2.imshow("source", frame)
    # frame=frame[cut_y_offset:550,cut_x_offset:850]
    # cv2.imshow("cut", frame)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if isFirstShow:
        isFirstShow = False
        showimg(img)
    # endregion
    thimg = imgRoundDect(img)  # 二值化
    cv2.imshow("Thred", thimg)
    # TODO 抗锯齿
    # thimg=cv2.medianBlur(thimg,ksize=21)
    # cv2.imshow("thred", thimg)
    # drawCont(thimg)median = cv2.medianBlur(img,5)

    # drawCont(thimg)
    # region 往复判断
    X, Y = drawCenterPoint(thimg)

    if LastX == 0:
        LastX = X
        DireX = signal(X - LastX)
    if LastY == 0:
        LastY = Y
        DireY = signal(Y - LastY)
    # print(X-LastX)
    if (X - LastX) * DireX < 0 and time.time() - LastTime > 0.5:
        couter = couter + 1
        DireX = -DireX
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

cap.release()
cv2.destroyAllWindows()
print(f"真实摆长:{Lresult}cm,摆线长度:{Lresult - 7.5}cm")

#=====Send Result to Terminal=====

# mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = '169.254.93.228'
# port = 32768
#
# try:
#     mySocket.connect((host, port))  ##连接到服务器
#     print("Connected")
# except:  ##连接不成功，运行最初的ip
#     print('Offline')
#
#
# msg = str(Lresult - 7.5)+","
# msg = msg+str(XMAX-XMIN)
# mySocket.send(msg.encode("utf-8"))
#
# print("Sent")
# mySocket.close()