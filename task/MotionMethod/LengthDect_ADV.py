import winsound
import sys
from task.myopencvTool import *

# input("Press Enter To Start")
# 620x480
ProgramStartTime = time.time()
ObjectLength = 10
ObjectLengthLong = 10
ObjectLengthShort = 7.5

# region Control Varibles
LastX = -1
DireX = 1
Ttime = []
# endregion
Lresult = 0

framesReadCounter = 0
FPS = 45
camera = CamerSystem()

while True:
    if time.time() - ProgramStartTime > 23:
        break
    frame = camera.MotionThreshold_l()
    framesReadCounter = framesReadCounter + 1

    # region 往复判断
    X, Y = drawCenterPoint(frame, "center")
    if LastX == -1:
        LastX = X
    # print(X-LastX)
    if (X - LastX) * DireX < -1 and framesReadCounter > 25:
        DireX = -DireX

        Ttime.append(framesReadCounter * (1.0 / FPS))
        framesReadCounter = 0
        print(f"T is {Ttime[-1]}")
        # Lresult = Time2Length(2 * np.mean(Ttime)) * 100
        print(f"L is {Time2Length(2 * Ttime[-1]) * 100} cm")
    LastX = X
    # endreigon
    # region Esc Key Halt
    k = cv2.waitKey(1)
    if k == 27:
        break
    # endregion

camera.releasCam()
cv2.destroyAllWindows()
Lresult = Time2Length(2 * np.mean(Ttime[2:])) * 100
if Lresult<120:
    RealL=Lresult-ObjectLengthShort
else:
    RealL=Lresult-ObjectLengthLong
print(f"真实摆长:{Lresult}cm,摆线长度:{RealL}cm")
winsound.Beep(6000, 2000)
