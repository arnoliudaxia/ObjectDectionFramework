from toolbox.opencvFramework import *
#有固定的背景https://www.yyearth.com/article/18-09/242.html

camer=CamerSystem()

# fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
# fgbg=cv.createBackgroundSubtractorMOG2(detectShadows=False,varThreshold=20)
# fgbg =cv2.createBackgroundSubtractorKNN()
fgbg=cv2.createBackgroundSubtractorMOG2(varThreshold=25,detectShadows=False)
cv2.namedWindow('ColorFilter')
def notiong(arg):
    pass
cv2.createTrackbar("iter","ColorFilter",0,5,notiong)
while True:
    ori=camer.takeImg()
    if ori is False:
        break
    frame=cv2.GaussianBlur(ori.copy(),(3,3),0)


    fgmask = fgbg.apply(frame)
    cv2.imshow("diff",ori&cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR) )
    fgmask=open_mor(fgmask,3,int(cv2.getTrackbarPos("iter","ColorFilter")))
    cv2.imshow("erode",fgmask)

    drawCenterPoint(fgmask.copy(),"CenterOfMask")


    ###
    (x, y, w, h) = camer.GetCenterByLongestContour(img=fgmask, type=ProcessType.Bound)
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