#此程序是调整Color Mask 的参数的
import cv2 as cv
import numpy as np
from task.myopencvTool import *



cap = cv.VideoCapture(2)
color_m=(0,0,255)

f = open("color.ini", "r")
ini=f.readline().split(" ")
icol =[int(i) for i in ini]  # Red


#创建窗体动态调参
def nothing(*arg):
        pass
cv2.namedWindow('colorTest',cv2.WINDOW_NORMAL)
# Lower range colour sliders.
cv2.createTrackbar('lowR', 'colorTest', icol[2], 255, nothing)
cv2.createTrackbar('lowG', 'colorTest', icol[1], 255, nothing)
cv2.createTrackbar('lowB', 'colorTest', icol[0], 255, nothing)
# Higher range colour sliders.
cv2.createTrackbar('highR', 'colorTest', icol[5], 255, nothing)
cv2.createTrackbar('highG', 'colorTest', icol[4], 255, nothing)
cv2.createTrackbar('highB', 'colorTest', icol[3], 255, nothing)


while True:

    lowR = cv2.getTrackbarPos('lowR', 'colorTest')
    lowG = cv2.getTrackbarPos('lowG', 'colorTest')
    lowB = cv2.getTrackbarPos('lowB', 'colorTest')
    highR = cv2.getTrackbarPos('highR', 'colorTest')
    highG = cv2.getTrackbarPos('highG', 'colorTest')
    highB = cv2.getTrackbarPos('highB', 'colorTest')

    # 读取
    ret, frame = cap.read()
    # frame = cv.resize(frame, (500, 500), interpolation=cv.INTER_CUBIC)
    frame = cv2.GaussianBlur(frame, (7, 7), 0)
    frame = cv2.medianBlur(frame, 7)
    cv.imshow("source", frame)
    frame_motion=frame
    # frameBGR = cv2.bilateralFilter(frameBGR, 15 ,75, 75)

    # 颜色过滤器
    lower_red=np.array([lowB,lowG,lowR])
    upper_red=np.array([highB,highG,highR])
    color_fliter = cv.inRange(frame_motion, lower_red, upper_red)
    cv.imshow("Color", color_fliter)

    k = cv.waitKey(1)
    if k == 27:
        break
    if k==ord("s"):
        f = open("color.ini", "w")
        inicon=[lowB,lowG,lowR,highB,highG,highR]
        f.write(" ".join([str(i) for i in inicon]))
        f.close()
        break

cap.release()
cv.destroyAllWindows()