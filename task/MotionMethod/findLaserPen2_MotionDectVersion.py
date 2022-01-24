from toolbox.opencvFramework import *
#有固定的背景https://www.yyearth.com/article/18-09/242.html

camer=CamerSystem()
cap = camer.cap_l

#尝试

# fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
# fgbg=cv.createBackgroundSubtractorMOG2(detectShadows=False,varThreshold=20)
# fgbg =cv2.createBackgroundSubtractorKNN()
fgbg=cv2.createBackgroundSubtractorMOG2(history=,varThreshold=16,detectShadows=False)

Lx=0
Ly=0
Lw=0
Lh=0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    fgmask = fgbg.apply(frame)
    # # cv.imshow("MaskMOG",fgmask )
    drawCenterPoint(fgmask.copy(),"CenterOfMask")
    # fgmask=camer.MotionThreshold_l()




    # cv.imshow("Thre",draw1 )
    # draw1=open_mor(fgmask,3,1)
    # draw1 = cv.dilate(draw1, kernel, iterations=3)
    # cv.imshow("OPENED",draw1)

    if sys.platform.startswith('win'):
        contours_m, hierarchy_m = cv.findContours(fgmask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    else:
        h,contours_m, hierarchy_m = cv.findContours(fgmask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    NoSat=True
    for c in contours_m:
        # print(cv.contourArea(c))
        if cv.contourArea(c) < 1000:
            continue
        NoSat=False
        (Lx,Ly,Lw,Lh)=(x, y, w, h) = cv.boundingRect(c)
        cv.rectangle(frame, (x, y), (x + w, y + h), color_m, 2)
    if NoSat:
        cv.rectangle(frame, (Lx, Ly), (Lx + Lw, Ly + Lh), color_m, 2)
    # Center Cross Line
    CenterCor=(320,240)
    cv2.line(frame,(320,220),(320,260),(0,0,255),2)
    cv2.line(frame,(300,240),(340,240),(0,0,255),2)
    cv.imshow("apply", frame)
    k = cv.waitKey(1)
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()