import cv2 as cv
import numpy as np

file_test = r"http://192.168.0.101:8080/?action=stream"
cap = cv.VideoCapture(file_test)

while True:
    # 读取一帧
    ret, frame = cap.read()
    # 如果视频结束，跳出循环
    if not ret:
        break
    cv.imshow("source", frame)
    k = cv.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
