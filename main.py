import os

import cv2, numpy as np
import matplotlib.pyplot as plt
from cv2 import mean


def showimg(img):
    plt.imshow(img, "gray")
    plt.show()
# ===Img Show Area ===
def imgRoundDect(img):
    ret, thre_img1 = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
    return 255-thre_img1
def imgCanny(img):
    canny = cv2.Canny(img, 200, 255)
    showimg(canny)
def readAllImgs(imglist,floder):
    imgname = os.listdir(floder)
    for imgn in imgname:
        URL=floder+"/"+imgn
        imglist.append(cv2.imread(URL,cv2.IMREAD_GRAYSCALE))
#计算二值化图像中有数据图像的中心点
def meanPoint(thimg):
    contours, hierarchy = cv2.findContours(thimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours[0].resize(contours[0].shape[0], 2)
    avr_x, avr_y = np.mean(contours[0], axis=0)
    return int(avr_x),int(avr_y)
#开运算操作
def open_mor(src):
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(src,cv2.MORPH_OPEN,kernel, iterations=3) #iterations进行3次操作
    cv2.imshow('open',opening)
    return opening

#边界填充算法
#以下以一张小图片的边界填充为示例
floderPath=r"C:\Users\Arnoliu\PycharmProjects\opecvtry\testcase\test\left"
testIMGlist=[]
readAllImgs(testIMGlist,floderPath)
for img in testIMGlist:
    showimg(img)
    # img_area = img[400:700, 300:700] #Middle
    img = img[150:250, 200:400] #Left
    thimg=imgRoundDect(img)
    # showimg(thimg)
    contours, hierarchy = cv2.findContours(thimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours[0].resize(contours[0].shape[0], 2)
    img_rgb = cv2.cvtColor(thimg, cv2.COLOR_GRAY2BGR)
    for point in contours[0]:
        cv2.circle(img_rgb, point, 1, (0, 0, 255))

    plt.imshow(img_rgb)
    plt.show()