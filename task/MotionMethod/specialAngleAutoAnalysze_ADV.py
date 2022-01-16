from task.myopencvTool import *
import winsound

ProgramStartTime = time.time()
ObjectLength = 10
# 620x480
cam = CamerSystem()
cap = -1

# region 控制变量
isFirstShow = True
LastX = -1
DireX = 1
Ttime = []
# endregion
Lresult = 0

# 首先要看看应该用哪个
frameCounter = 0
FPS = 45

l_XMIN = float("inf")
l_XMAX = -l_XMIN
r_XMIN = float("inf")
r_XMAX = -r_XMIN

RangeXChangement = 0
# input("Press Enter To Start")
while True:
    if frameCounter > 60:
        if l_XMAX - l_XMIN > r_XMAX - r_XMIN:
            cap = 1
        else:
            cap = 2
        break

    frame_l, frame_r = cam.MotionThreshold()
    frameCounter = frameCounter + 1

    X_l, Y = centerPoint(frame_l)
    X_r, Y = centerPoint(frame_r)

    l_XMIN = min(l_XMIN, X_l)
    l_XMAX = max(l_XMAX, X_l)
    r_XMIN = min(r_XMIN, X_r)
    r_XMAX = max(r_XMAX, X_r)
frameCounter = 0
while True:
    if time.time() - ProgramStartTime > 23:
        break
    thimg = cam.MotionThreshold()[cap - 1]
    frameCounter = frameCounter + 1
    cv2.imshow("Thred", thimg)

    X, Y = drawCenterPoint(thimg, "c")

    if LastX == -1:
        LastX = X
    # print(X-LastX)
    if (X - LastX) * DireX < -1 and frameCounter > 25:
        DireX = -DireX

        Ttime.append(frameCounter * (1.0 / FPS))
        frameCounter = 0
        print(f"T is {Ttime[-1]}")
        # Lresult = Time2Length(2 * np.mean(Ttime)) * 100
        print(f"L is {Time2Length(2 * Ttime[-1]) * 100} cm")
    LastX = X
    # endreigon
    # region 按Esc键退出
    k = cv2.waitKey(1)
    if k == 27:
        break
    # endregion

cam.releasCam()
cv2.destroyAllWindows()
Lresult = Time2Length(2 * np.mean(Ttime[2:])) * 100
print(f"真实摆长:{Lresult}cm,摆线长度:{Lresult - ObjectLength}cm")
winsound.Beep(6000, 2000)
