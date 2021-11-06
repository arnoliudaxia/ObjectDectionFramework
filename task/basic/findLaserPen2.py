import cv2
import numpy as np
import matplotlib.pyplot as plt
import time


#1280x720 10 FPS
file_test = r"http://169.254.121.50:8080/?action=stream"
cap = cv2.VideoCapture(file_test)

cut_x_offset = 400
cut_y_offset = 300
#region 模块化算法
def showimg(img):
    plt.imshow(img, "gray")
    plt.show()
def imgRoundDect(img):
    ret, thre_img1 = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
    return 255-thre_img1
#计算二值化图像中有数据图像的中心点
def findRealCont(thimg):
    contours, hierarchy = cv2.findContours(thimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    finalCon=contours[0]
    for con in contours:
        if cv2.contourArea(con)<1000:
            continue
        else:
            finalCon=con
    finalCon.resize(finalCon.shape[0], 2)
    return finalCon

def drawBox(thimg,orignimg):
    tempimg=thimg.copy()
    contours=findRealCont(tempimg)
    (x, y, w, h) =cv2.boundingRect(contours)
    img_rgb = cv2.cvtColor(tempimg, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(img_rgb, (x, y), (x + w, y + h), (0,0,255), 2)
    cv2.rectangle(orignimg, (x+cut_x_offset, y+cut_y_offset), (x + w+cut_x_offset, y +h+cut_y_offset), (0,0,255), 2)
    # cv2.imshow("middleProcudure",img_rgb)
    cv2.imshow("finalImg",orignimg)

#endregion
isFirstShow=True
while True:
    # 读取一帧
    ret, frame = cap.read()
    # 如果视频结束，跳出循环
    if not ret:
        break

    # cv2.imshow("source", frame)
    frame_cut=frame[cut_y_offset:550,cut_x_offset:850]
    # cv2.imshow("cut", frame)
    img=cv2.cvtColor(frame_cut,cv2.COLOR_BGR2GRAY)

    if isFirstShow:
        isFirstShow=False
        showimg(frame)
        showimg(frame_cut)
    thimg=imgRoundDect(img)
    drawBox(thimg,frame)

    #region 按Esc键退出
    k = cv2.waitKey(1)
    if k == 27:
        break
    #endregion


cap.release()
cv2.destroyAllWindows()
