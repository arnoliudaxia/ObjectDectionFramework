import cv2 as cv
file_test = r"C:\Users\Arnoliu\PycharmProjects\opecvtry\testcase\WIN_20220113_17_57_44_Pro.mp4"
cap = cv.VideoCapture(file_test)
while True:
    # 读取一帧
    ret, frame = cap.read()
    # 如果视频结束，跳出循环
    if not ret:
        break
    cv.imshow("source", frame)
    k = cv.waitKey(10)
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()