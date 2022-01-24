from toolbox.opencvFramework import *
import toolbox.setting as setting


def runMotionCailbrate():
    camer = CamerSystem()

    # fgbg=cv2.bgsegm.createBackgroundSubtractorGMG()
    fgbg = cv2.createBackgroundSubtractorKNN(history=100, detectShadows=False)
    # fgbg = cv2.createBackgroundSubtractorMOG2(history=100,varThreshold=25, detectShadows=False)
    cv2.namedWindow('ColorFilter')
    cv2.createTrackbar("kernel", "ColorFilter", readMotionIni()[0], 8, lambda x: setting.saveMotionini(kernelSize=x))
    cv2.createTrackbar("iter", "ColorFilter", readMotionIni()[1], 5, lambda x: setting.saveMotionini(iterations=x))




    while True:
        ori = camer.takeImg()
        if ori is None:
            break
        frame = cv2.GaussianBlur(ori.copy(), (3, 3), 0)

        fgmask = fgbg.apply(frame)
        fgmask = open_mor(fgmask, int(cv2.getTrackbarPos("kernel", "ColorFilter")),
                          int(cv2.getTrackbarPos("iter", "ColorFilter")))
        cv2.imshow("diff", ori & cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR))
        # cv2.imshow("erode", fgmask)

        ###
        (x, y, w, h) = camer.GetCenterByLongestContour(img=fgmask, type=ProcessType.Bound)
        if x == -1:
            continue
        cv2.rectangle(ori, (x, y), (x + w, y + h), (0, 0, 255), 2)
        X, Y = round((2 * x + w) / 2), round((2 * y + h) / 2)
        # 绘制中心十字线
        centerRreference = (320, 240)
        cv2.line(ori, (320, 220), (320, 260), (0, 0, 255), 2)
        cv2.line(ori, (300, 240), (340, 240), (0, 0, 255), 2)
        # cv2.line(ori, (X,Y+20), (X,Y-20), (0, 0, 255), 2)
        # cv2.line(ori, (X+20,Y), (X-20,Y), (0, 0, 255), 2)
        cv2.imshow("Target", ori)

        if cv2.waitKey(int(1000 / camer.getFPS())) == 27:
            break

    camer.releasCam()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    runMotionCailbrate()
