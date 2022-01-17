from toolbox.opencvFramework import *
from toolbox.mathUtility import *

camS=CamerSystem()
timer=Timer()

f=open("data.txt","w")
while True:
    frame=camS.ColorThreshold(showSource=True)
    if frame is None:
        break
    x, y =camS.GetCenterByLongestContour(img=frame,type=ProcessType.CenterCoordinate,debug=True)
    if not f.writable():
        print("File is occupied!Check access!")
    f.write(",".join([str(round(i,2)) for i in(x,y,timer.TimePast())])+"\n")

    k = cv2.waitKey(int(1000 / camS.getFPS()))
    if k == 27:
        break

camS.releasCam()
cv2.destroyAllWindows()
f.close()
