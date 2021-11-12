# import winsound
import math
import sys
import os
from task.myopencvTool import *

# input("Press Enter To Start")
# 620x480
ProgramStartTime = time.time()

# ObjectLength = 10
# ObjectLengthLong = 10
# ObjectLengthShort = 7.75
# ObjectLengthVeryShort = -4
# region Control Varibles
LastX = -1
DireX = 0
Ttime = []
# endregion
Lresult = 0

framesReadCounter = 0
camera = CamerSystem()
LastTime=time.time()
while True:
    if time.time() - ProgramStartTime > 28:
        break
    frame = camera.MotionThreshold_l()
    framesReadCounter = framesReadCounter + 1

    # region 往复判断
    X, Y = drawCenterPoint(frame, "center")
    # print(X)

    # X, Y = centerPoint(frame)
    if LastX == -1:
        LastX = X
    if DireX == 0:
        DireX = signal(X-320)
    # print(X-LastX)
    print(X-320)
    if DireX*(X-320)<=0 :
        # if time.time()-LastTime<0.7:
        #     continue
        Ttime.append(time.time()-LastTime)
        LastTime=time.time()
        print("T is ")
        print(Ttime[-1])
        if len(Ttime)>3:
            print("T mean is:")
            print(np.mean(Ttime[2:]))
        # print(f"T is {Ttime[-1]}")
        # Lresult = Time2Length(2 * np.mean(Ttime)) * 100
        print("L is ")
        print(Time2Length(2 * Ttime[-1]) * 100)
    DireX = signal(X-320)
    # endreigon
    # region Esc Key Halt
    k = cv2.waitKey(1)
    if k == 27:
        break
    # endregion

camera.releasCam()
cv2.destroyAllWindows()
Lresult = Time2Length(2 * np.mean(Ttime[2:])) * 100
# if Lresult>100:#vERY OK
#     RealL=Lresult-ObjectLengthLong
# # elif Lresult<120:
# #     RealL=Lresult-ObjectLengthShort
# else:
#     RealL=Lresult-ObjectLengthShort
RealL=fixFunction(Lresult)
# RealL=Lresult-ObjectLengthShort
print("Real Length(cm):")
print(Lresult)
print("The length of line(cm):")
print(RealL)
os.system("play /home/upsquared/Downloads/applause.mp3")
# print(f"真实摆长:{Lresult}cm,摆线长度:{RealL}cm")
# winsound.Beep(6000, 2000)
