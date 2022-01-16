import time
import os
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

objectLengthFix = 0
AngleFix = 0
cameraNumber=2
cameraNumber2=0
# r"http://192.168.0.120:8080/?action=stream"
iniURL=r"task/Color/color.ini"


# ===MathAndPhysic ===
def signal(intput):
    if intput >= 0:
        return 1
    if intput < 0:
        return -1


def angleCal(x, y):
    if x != 0 and y != 0:
        return math.atan(x / y) * 180 / math.pi


def Time2Length(time):
    return time ** 2 * 9.886 / (4 * math.pi ** 2)


def fixFunction(inputv):
    return inputv - math.log(10, inputv / 10) * 8.5


# ===OpenCVAPI ===
# ==Basic==
def showimgInPanel(img):
    plt.imshow(img, "gray")
    plt.show()

def readIni():
    f = open(iniURL, "r")
    ini = f.readline().split(" ")
    icol = [int(i) for i in ini]
    lower_red = np.array(icol[0:3])
    upper_red = np.array(icol[3:])
    return lower_red,upper_red
class CamerSystem:
    fgbg = cv2.createBackgroundSubtractorKNN()

    def __init__(self,oneOrTwoCamera):
        # 根据用户的选择开启几个摄像头
        self.CameraNumber=oneOrTwoCamera
        assert oneOrTwoCamera!=1 or oneOrTwoCamera!=2
        if oneOrTwoCamera>=1:
            self.cap_l = cv2.VideoCapture(cameraNumber)
        if oneOrTwoCamera==2:
            self.cap_r = cv2.VideoCapture(cameraNumber2)
        self.lower_red,self.upper_red=readIni()
    # Read Img with MotionDect
    def releasCam(self):
        if self.CameraNumber >= 1:
            self.cap_l.release()
        if self.CameraNumber == 2:
            self.cap_r.release()

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

    def ColorThreshold(self):
        lower_red = self.lower_red
        upper_red = self.upper_red
        ret, frame = self.cap_l.read()
        # frame = cv.resize(frame, (500, 500), interpolation=cv.INTER_CUBIC)
        frame = cv2.GaussianBlur(frame, (7, 7), 0)
        frame = cv2.medianBlur(frame, 7)

        color_fliter = cv2.inRange(frame, lower_red, upper_red)

        color_fliter = close_mor(color_fliter, 10, 3)
        closedMask = open_mor(color_fliter, 5, 1)

        return closedMask
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



# ===Python Util===
class Timer:

    def __init__(self):
        self.clock=time.time()

    def Update(self):
        step = time.time() - self.clock
        print(f"Time step : {step}; FPS:{int(1.0/step)}")
        self.clock = time.time()
    def TimePast(self):
        return time.time()-self.clock