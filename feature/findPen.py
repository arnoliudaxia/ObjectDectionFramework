from toolbox.opencvFramework import *

#mode 1:Color
def runFindPen(mode:int):
    camS=CamerSystem()

    while True:
        if mode==1:
            ori,frame=camS.ColorThreshold(keepOrigin=True,showSource=False)
            if frame is None:
                break
            (x, y, w, h) =camS.GetCenterByLongestContour(img=frame,type=ProcessType.Bound)

        #MotionMethodTest


        ###
        cv2.rectangle(ori, (x, y), (x + w, y + h), (0,0,255), 2)
        X, Y = round((2 * x + w) / 2), round((2 * y + h) / 2)
        #绘制中心十字线
        centerRreference=(320,240)
        cv2.line(ori, (320, 220), (320, 260), (0, 0, 255), 2)
        cv2.line(ori, (300, 240), (340, 240), (0, 0, 255), 2)
        # cv2.line(ori, (X,Y+20), (X,Y-20), (0, 0, 255), 2)
        # cv2.line(ori, (X+20,Y), (X-20,Y), (0, 0, 255), 2)
        cv2.imshow("Target", ori)

        k = cv2.waitKey(int(1000 / camS.getFPS()))
        if k == 27:
            break

    camS.releasCam()
    cv2.destroyAllWindows()
