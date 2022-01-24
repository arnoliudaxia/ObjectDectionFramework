# 此程序是调整Color Mask 的参数的
from toolbox.opencvFramework import *
#https://github.com/1zlab/1ZLAB_Color_Block_Finder

def runColorConfigure():
    cam = CamerSystem()
    low, high = readColorIni()
    icol = low.tolist() + high.tolist()

    # region 创建窗体
    # 创建空回调函数
    def nothing(*arg):
        pass

    cv2.namedWindow('ColorFilter', cv2.WINDOW_NORMAL)
    cv2.createTrackbar("speed(%)", "ColorFilter", 100, 200, nothing)
    # Lower range colour sliders.
    cv2.createTrackbar('lowR', 'ColorFilter', icol[2], 255, nothing)
    cv2.createTrackbar('lowG', 'ColorFilter', icol[1], 255, nothing)
    cv2.createTrackbar('lowB', 'ColorFilter', icol[0], 255, nothing)
    # Higher range colour sliders.
    cv2.createTrackbar('highR', 'ColorFilter', icol[5], 255, nothing)
    cv2.createTrackbar('highG', 'ColorFilter', icol[4], 255, nothing)
    cv2.createTrackbar('highB', 'ColorFilter', icol[3], 255, nothing)

    cv2.createTrackbar("Save", 'ColorFilter', 0, 1, nothing)

    # endregion
    while True:

        lowR = cv2.getTrackbarPos('lowR', 'ColorFilter')
        lowG = cv2.getTrackbarPos('lowG', 'ColorFilter')
        lowB = cv2.getTrackbarPos('lowB', 'ColorFilter')
        highR = cv2.getTrackbarPos('highR', 'ColorFilter')
        highG = cv2.getTrackbarPos('highG', 'ColorFilter')
        highB = cv2.getTrackbarPos('highB', 'ColorFilter')
        speed = cv2.getTrackbarPos('speed(%)', 'ColorFilter')

        # 颜色过滤器
        lower_red = np.array([lowB, lowG, lowR])
        upper_red = np.array([highB, highG, highR])
        ori,frame = cam.ColorThreshold(colorBound=[lower_red, upper_red],keepOrigin=True)
        if frame is None:
            cam.releasCam()
            cam = CamerSystem()
            continue
        cv2.imshow("ColorFilter", ori&cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR))

        k = cv2.waitKey(int(1000 / cam.getFPS() / ((speed + 1) / 100)))
        if k == 27:
            break
        if k == ord("s") or cv2.getTrackbarPos("Save",'ColorFilter')==1:
            saveColorini([[lowB, lowG, lowR], [highB, highG, highR]])
            break

    cam.releasCam()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    runColorConfigure()