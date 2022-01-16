import cv2
import numpy as np

from task.myopencvTool import *



cap = cv2.VideoCapture(2)
color_m=(0,0,255)#外边框颜色
f = open("color.ini", "r")
ini=f.readline().split(" ")
icol =[int(i) for i in ini]    # Red
lower_red = np.array(icol[0:3])
upper_red = np.array(icol[3:])



while True:

    # 读取
    ret, frame = cap.read()
    # frame = cv2.resize(frame, (500, 500), interpolation=cv2.INTER_CUBIC)
    frame = cv2.GaussianBlur(frame, (7, 7), 0)
    frame = cv2.medianBlur(frame, 7)
    cv2.imshow("source", frame)
    frame_motion=frame
    # frameBGR = cv2.bilateralFilter(frameBGR, 15 ,75, 75)

    # 颜色过滤器

    color_fliter = cv2.inRange(frame_motion, lower_red, upper_red)
    cv2.imshow("Color", color_fliter)

    color_fliter=close_mor(color_fliter,10,3)
    closedMask = open_mor(color_fliter, 5, 1)
    drawCenterPoint(closedMask.copy(),"Closed")

    if sys.platform.startswith('win'):
        contours_m, hierarchy_m = cv2.findContours(closedMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        h, contours_m, hierarchy_m = cv2.findContours(closedMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    areas=[cv2.contourArea(c) for c in contours_m]
    longestArea=contours_m[np.nanargmax(areas)]
    (x, y, w, h) = cv2.boundingRect(longestArea)
    cv2.rectangle(frame_motion, (x, y), (x + w, y + h), color_m, 2)
    X, Y = round((2 * x + w) / 2), round((2 * y + h) / 2)
    frame_motion = cv2.circle(frame_motion, (X, Y), 2, (255, 0, 0))
    #绘制中心十字线
    cv2.line(frame_motion, (320, 220), (320, 260), (0, 0, 255), 2)
    cv2.line(frame_motion, (300, 240), (340, 240), (0, 0, 255), 2)
    cv2.imshow("HH", frame_motion)

    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()