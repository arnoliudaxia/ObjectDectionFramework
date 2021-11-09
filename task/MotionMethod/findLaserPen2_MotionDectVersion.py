import cv2 as cv
import numpy as np
from task.myopencvTool import *

input("Press Enter To Start")

camer=CamerSystem()
cap = camer.cap_l

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (2, 2))
color_m = (0, 0, 255)

# fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
# fgbg=cv.createBackgroundSubtractorMOG2(detectShadows=False,varThreshold=20)
fgbg =cv.createBackgroundSubtractorKNN()


Lx=0
Ly=0
Lw=0
Lh=0
while True:
    ret, frame = cap.read()
    # if not ret:
    #     break
    # # frame = cv.resize(frame, (500, 500), interpolation=cv.INTER_CUBIC)
    # frame_motion = frame.copy()
    # # cv.imshow("source", frame_motion)

    fgmask = fgbg.apply(frame)
    # # cv.imshow("MaskMOG",fgmask )
    drawCenterPoint(fgmask.copy(),"CenterOfMask")
    # fgmask=camer.MotionThreshold_l()




    # cv.imshow("Thre",draw1 )
    # draw1=open_mor(fgmask,3,1)
    # draw1 = cv.dilate(draw1, kernel, iterations=3)
    # cv.imshow("OPENED",draw1)

    l,contours_m, hierarchy_m = cv.findContours(fgmask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    NoSat=True
    for c in contours_m:
        # print(cv.contourArea(c))
        if cv.contourArea(c) < 1000:
            continue
        NoSat=False
        (Lx,Ly,Lw,Lh)=(x, y, w, h) = cv.boundingRect(c)
        cv.rectangle(frame, (x, y), (x + w, y + h), color_m, 2)
    if NoSat:
        cv.rectangle(frame, (Lx, Ly), (Lx + Lw, Ly + Lh), color_m, 2)
    cv.imshow("apply", frame)
    k = cv.waitKey(1)
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()