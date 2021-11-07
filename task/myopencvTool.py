import time
import os

import cv2
import numpy as np
import matplotlib.pyplot as plt
import math


# ===MathAndPhysic ===
def signal(intput):
    if intput >= 0:
        return 1
    if intput < 0:
        return -1
def angleCal(x,y):
    if x!=0 and y!=0:
        return math.atan(x/y)*180/math.pi
def Time2Length(time):
    return time ** 2 * 9.886 / (4 * math.pi ** 2)


# ===OpenCVAPI ===
# ==Basic==
def readAllImgs(imglist,floder):
    imgName = os.listdir(floder)
    for imgn in imgName:
        URL=floder+"/"+imgn
        imglist.append(cv2.imread(URL,cv2.IMREAD_GRAYSCALE))
def showimgInPanel(img):
    plt.imshow(img, "gray")
    plt.show()

class CamerSystem:
    #Read Img and simple process
    cap_l = cv2.VideoCapture(r"http://169.254.121.50:8080/?action=stream")
    cap_r = cv2.VideoCapture(r"http://169.254.3.16:8080/?action=stream")
    #Read Img with MotionDect
    def releasCam(self):
        self.cap_l.release()
        self.cap_r.release()

    fgbg =cv2.createBackgroundSubtractorKNN()
    def MotionThreshold(self):
        ret, frame = self.cap_l.read()
        ret, frame_r = self.cap_r.read()
        fgmask = CamerSystem.fgbg.apply(frame)
        fgmask_r = CamerSystem.fgbg.apply(frame_r)
        # drawCenterPoint(fgmask, "CenterOfMask1")
        # drawCenterPoint(fgmask_r, "CenterOfMask2")

        fgmask = open_mor(fgmask, 2, 1)
        fgmask_r = open_mor(fgmask_r, 2, 1)
        fgmask = close_mor(fgmask, 25, 3)
        fgmask_r = close_mor(fgmask_r, 25, 3)
        return fgmask,fgmask_r


    def ColorThreshold(self):
        lower_red = np.array([25, 5, 80])
        upper_red = np.array([60, 30, 125])

#Open And Close
def open_mor(src,kernelsize,iter):
    kernel = np.ones((kernelsize,kernelsize),np.uint8)
    opening = cv2.morphologyEx(src,cv2.MORPH_OPEN,kernel, iterations=iter) #iterations进行3次操作
    # cv.imshow('open',opening)
    return opening
def close_mor(src,kernelsize,iter):
    kernel = np.ones((kernelsize,kernelsize),np.uint8)
    opening = cv2.morphologyEx(src,cv2.MORPH_CLOSE,kernel, iterations=iter) #iterations进行3次操作
    # cv.imshow('open',opening)
    return opening
#Threshold
def imgThresholdEasy(img):
    ret, thre_img1 = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
    return 255 - thre_img1
def imgThresholdCust(img,val):
    ret, thre_img1 = cv2.threshold(img, val, 255, cv2.THRESH_BINARY)
    return 255 - thre_img1
def imgThresholdAuto(img):
    ret, thre_img1 = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
    return 255-thre_img1
def imgThresholdCanny(img):
    return cv2.Canny(img, 200, 255)# TODO Parameter


def centerPoint(thimg):
    mom = cv2.moments(thimg)
    if mom["m00"]==0:
        return 0,0
    center_x = int(mom["m10"] / mom["m00"])
    center_y = int(mom["m01"] / mom["m00"])
    return center_x, center_y

#Draw Tool
def drawPointonImg(img, px, py):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.circle(img_rgb, (px, py), 3, (0, 0, 255))
    cv2.imshow("centerPoint", img_rgb)
def drawCenterPoint(img,imgName):
    meanX, meanY = centerPoint(img)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.circle(img_rgb, (meanX, meanY), 3, (0, 0, 255))
    cv2.imshow("centerPoint"+str(imgName), img_rgb)
    return meanX, meanY

def findRealCont(thimg):
    contours, hierarchy = cv2.findContours(thimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    finalCon = contours[0]
    for con in contours:
        if cv2.contourArea(con) < 1000:
            continue
        else:
            finalCon = con
    finalCon.resize(finalCon.shape[0], 2)
    return finalCon, thimg
def drawCont(thimg):
    tempimg = thimg.copy()
    contours = findRealCont(tempimg)
    img_rgb = cv2.cvtColor(tempimg, cv2.COLOR_GRAY2BGR)
    for point in contours:
        cv2.circle(tempimg, point, 1, (0, 0, 255))
    cv2.imshow("Cont", tempimg)
def meanPointOfContour(thimg):
    contours = findRealCont(thimg)
    avr_x, avr_y = np.mean(contours, axis=0)
    return int(avr_x), int(avr_y)

#===Python Util===
class Timer:
    clock=time.time()

    def Update(self):
        step=time.time()-self.clock
        print(f"Time step : {step}; FPS:{int(1.0/step)}")
        self.clock=time.time()