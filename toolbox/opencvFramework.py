import os
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from .setting import *


objectLengthFix = 0
AngleFix = 0

#网络摄像头URL示例 r"http://192.168.0.120:8080/?action=stream"
cameraMainURL=r"C:\Users\Arnoliu\PycharmProjects\opecvtry\testcase\WIN_20220113_17_57_44_Pro.mp4"
cameraViceURL=0


# ===OpenCVAPI ===
# ==Basic==
def showimgInPanel(img):
    plt.imshow(img, "gray")
    plt.show()



###########################################
class CamerSystem:
    fgbg = cv2.createBackgroundSubtractorKNN()

    def __init__(self,oneOrTwoCamera=1):
        # 根据用户的选择开启几个摄像头
        self.CameraNumber=oneOrTwoCamera
        assert oneOrTwoCamera!=1 or oneOrTwoCamera!=2
        if oneOrTwoCamera>=1:
            self.cap_l = cv2.VideoCapture(cameraMainURL)
        if oneOrTwoCamera==2:
            self.cap_r = cv2.VideoCapture(cameraViceURL)

    #读取配置文件
    def loadConfigue(self):
        self.lower_red,self.upper_red=readColorIni()

    def takeImg(self):
        ret, frame = self.cap_l.read()
        if not ret:
            print("No Stream or stream stopped!")
            return False
        return frame
    def getFPS(self):
        return self.cap_l.get(propId=cv2.CAP_PROP_FPS)
    def releasCam(self):
        if self.CameraNumber >= 1:
            self.cap_l.release()
        if self.CameraNumber == 2:
            self.cap_r.release()

    # Read Img with MotionDect
    def MotionThreshold(self):
        ret, frame = self.cap_l.read()
        ret, frame_r = self.cap_r.read()
        fgmask = CamerSystem.fgbg.apply(frame)
        fgmask_r = CamerSystem.fgbg.apply(frame_r)
        # drawCenterPoint(fgmask, "CenterOfMask1")
        # drawCenterPoint(fgmask_r, "CenterOfMask2")

        fgmask = open_mor(fgmask, 3, 1)
        fgmask_r = open_mor(fgmask_r, 3, 1)
        fgmask = close_mor(fgmask, 50, 1)
        fgmask_r = close_mor(fgmask_r, 50, 1)
        return fgmask, fgmask_r

    def MotionThreshold_l(self):
        ret, frame = self.cap_l.read()
        fgmask = CamerSystem.fgbg.apply(frame)
        # drawCenterPoint(fgmask, "CenterOfMask1")
        # drawCenterPoint(fgmask_r, "CenterOfMask2")

        fgmask = open_mor(fgmask, 3, 1)
        fgmask = close_mor(fgmask, 50, 1)
        return centerPoint(fgmask)
        # def MotionThreshold_l(self):
        #     ret, frame = self.cap_l.read()
        #     fgmask = CamerSystem.fgbg.apply(frame)
        #     # drawCenterPoint(fgmask, "CenterOfMask1")
        #     # drawCenterPoint(fgmask_r, "CenterOfMask2")

        #     fgmask = open_mor(fgmask, 3, 1)
        #     # fgmask = close_mor(fgmask, 50, 1)
        #     return fgmask
        # def SimpleCenter(self,img):
        # if sys.platform.startswith('win'):
        #     contours_m, hierarchy_m = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # else:
        #     h, contours_m, hierarchy_m = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # NoSat = True
        # for c in contours_m:
        #     # print(cv.contourArea(c))
        #     if cv2.contourArea(c) < 1000:
        #         continue
        #     NoSat = False
        #     (x, y, w, h) = cv2.boundingRect(c)
        #     return (x + w) / 2, (y + h) / 2
        #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        #     cv2.imshow("kuang", img)
        #     self.Lx = (x + w) / 2
        #     self.Ly = (y + h) / 2
        # if NoSat:
        #     return self.Lx, self.Ly

    def MotionThreshold_r(self):
        ret, frame = self.cap_r.read()
        fgmask = CamerSystem.fgbg.apply(frame)
        # drawCenterPoint(fgmask, "CenterOfMask1")
        # drawCenterPoint(fgmask_r, "CenterOfMask2")

        fgmask = open_mor(fgmask, 3, 1)
        fgmask = close_mor(fgmask, 50, 1)
        return centerPoint(fgmask)

    def ColorThreshold(self,blurKernelSize=5,colorBound=None,showSource=True):
        self.loadConfigue()
        if colorBound==None:
            lower_bound = self.lower_red
            upper_bound = self.upper_red
        else:
            lower_bound = colorBound[0]
            upper_bound = colorBound[1]

        frame=self.takeImg()
        if frame is None:
            return None
        if showSource:
            cv2.imshow("source", frame)
        frame = cv2.GaussianBlur(frame, (blurKernelSize, blurKernelSize), 0)
        color_fliter = cv2.inRange(frame, lower_bound, upper_bound)
        color_fliter= cv2.erode(color_fliter,(10,10),iterations=3)
        color_fliter = open_mor(color_fliter, 5, 1)

        return color_fliter
    def GetCenterByColor(self):
        closedMask=self.ColorThreshold()
        if sys.platform.startswith('win'):
            contours_m, hierarchy_m = cv2.findContours(closedMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            h, contours_m, hierarchy_m = cv2.findContours(closedMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        areas = [cv2.contourArea(c) for c in contours_m]
        longestArea = contours_m[np.nanargmax(areas)]
        (x, y, w, h) = cv2.boundingRect(longestArea)
        return round((2 * x + w) / 2), round((2 * y + h) / 2)




#region Open And Close
def open_mor(src, kernelsize, iter):
    kernel = np.ones((kernelsize, kernelsize), np.uint8)
    opening = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel, iterations=iter)
    return opening

#! Do not use this
def close_mor(src, kernelsize, iter):
    kernel = np.ones((kernelsize, kernelsize), np.uint8)
    opening = cv2.morphologyEx(src, cv2.MORPH_CLOSE, kernel, iterations=iter)
    return opening
#endregion
#直接计算图像的重心
def centerPoint(thimg):
    mom = cv2.moments(thimg)
    if mom["m00"] == 0:
        return 0, 0
    center_x = round(mom["m10"] / mom["m00"])
    center_y = round(mom["m01"] / mom["m00"])
    return center_x, center_y


# Draw Tool
def drawPointonImg(img, px, py):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.circle(img_rgb, (px, py), 3, (0, 0, 255))
    cv2.imshow("centerPoint", img_rgb)


def drawCenterPoint(img, imgName):
    meanX, meanY = centerPoint(img)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.circle(img_rgb, (meanX, meanY), 3, (0, 0, 255))
    cv2.imshow("centerPoint" + str(imgName), img_rgb)
    return meanX, meanY


def findRealCont(thimg):
    pass
    # if sys.platform.startswith('win'):
    #     contours_m, hierarchy_m = cv.findContours(fgmask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # else:
    #     h,contours_m, hierarchy_m = cv.findContours(fgmask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # finalCon = contours[0]
    # for con in contours:
    #     if cv2.contourArea(con) < 1000:
    #         continue
    #     else:
    #         finalCon = con
    # finalCon.resize(finalCon.shape[0], 2)
    # return finalCon, thimg


def drawCont(thimg):
    tempimg = thimg.copy()
    contours = findRealCont(tempimg)
    img_rgb = cv2.cvtColor(tempimg, cv2.COLOR_GRAY2BGR)
    for point in contours:
        cv2.circle(tempimg, point, 1, (0, 0, 255))
    cv2.imshow("Cont", tempimg)
