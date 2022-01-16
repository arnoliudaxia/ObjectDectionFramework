from toolbox.opencvFramework import *


camS=CamerSystem()

while True:
    ori,frame=camS.ColorThreshold(keepOrigin=True,showSource=False)
    if frame is None:
        break

    if sys.platform.startswith('win'):
        contours_m, hierarchy_m = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        h, contours_m, hierarchy_m = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    areas=[cv2.contourArea(c) for c in contours_m]
    longestArea=contours_m[np.nanargmax(areas)]
    (x, y, w, h) = cv2.boundingRect(longestArea)
    frame_motion=frame
    cv2.rectangle(ori, (x, y), (x + w, y + h), (0,0,255), 2)
    X, Y = round((2 * x + w) / 2), round((2 * y + h) / 2)
    # cv2.circle(ori, (X, Y), 2, (255, 0, 0))
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