import cv2
import numpy as np
import matplotlib.pyplot as plt
import math


# region MathAndPhysic
def signal(intput):
    if intput >= 0:
        return 1
    if intput < 0:
        return -1
def Time2Length(time):
    return time ** 2 * 9.886 / (4 * math.pi ** 2)
#endregion

def showimgInPanel(img):
    plt.imshow(img, "gray")
    plt.show()

def imgRoundDectEasy(img):
    ret, thre_img1 = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
    return 255 - thre_img1
#通过图像的矩计算中心点，仅仅适用于二值化图像主体有数据其他背景没有数据的情况
def centerPoint(thimg):
    mom = cv2.moments(thimg)
    center_x = int(mom["m10"] / mom["m00"])
    center_y = int(mom["m01"] / mom["m00"])
    return center_x, center_y


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