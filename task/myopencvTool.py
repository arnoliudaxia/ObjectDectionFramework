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
    if x!=0 and y!=0 and x!=y:
        return math.atan(x/y)*180/math.pi
def Time2Length(time):
    return time ** 2 * 9.886 / (4 * math.pi ** 2)

# ===OpenCVAPI ===
#Basic
def readAllImgs(imglist,floder):
    imgName = os.listdir(floder)
    for imgn in imgName:
        URL=floder+"/"+imgn
        imglist.append(cv2.imread(URL,cv2.IMREAD_GRAYSCALE))
def showimgInPanel(img):
    plt.imshow(img, "gray")
    plt.show()

#二值化方法
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

#通过图像的矩计算中心点，仅仅适用于二值化图像主体有数据其他背景没有数据的情况
def centerPoint(thimg):
    mom = cv2.moments(thimg)
    center_x = int(mom["m10"] / mom["m00"])
    center_y = int(mom["m01"] / mom["m00"])
    return center_x, center_y
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

def meanPointOfContour(thimg):
    contours = findRealCont(thimg)
    avr_x, avr_y = np.mean(contours, axis=0)
    return int(avr_x), int(avr_y)
#开运算操作
def open_mor(src,kernelSize,iters):
    kernel = np.ones((kernelSize,kernelSize),np.uint8)
    opening = cv2.morphologyEx(src,cv2.MORPH_OPEN,kernel, iterations=iters) #iterations进行3次操作
    cv2.imshow('open',opening)
    return opening

#===Python Util===
class Timer:
    clock=time.time()

    def Update(self):
        step=time.time()-self.clock
        print(f"Time step : {step}; FPS:{int(1.0/step)}")
        self.clock=time.time()