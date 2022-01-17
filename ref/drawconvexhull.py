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

    areas = [cv2.contourArea(c) for c in contours_m]
    longestArea = contours_m[np.nanargmax(areas)]
    hull = cv2.convexHull(longestArea)

    length = len(hull)
    for i in range(len(hull)):
        cv2.line(ori, tuple(hull[i][0]), tuple(hull[(i + 1) % length][0]), (0, 255, 0), 2)

    cv2.imshow("Target", ori)

    k = cv2.waitKey(int(1000 / camS.getFPS()))
    if k == 27:
        break

camS.releasCam()
cv2.destroyAllWindows()