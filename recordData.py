from toolbox.opencvFramework import *
from toolbox.mathUtility import *

def runRecordData(mode:int,matchMethod=0):
    camS=CamerSystem()
    timer=Timer()

    f=open("data.txt", "w")
    xposData=[]
    timeData=[]
    plt.ion()
    # plt.figure(1)
    while True:
        if mode!=3:
            frame=None
            if mode==1:
                frame=camS.ColorThreshold(showSource=True)
            elif mode==2:
                frame=camS.MotionThreshold()
            if frame is None:
                break
            x, y =camS.GetCenterByLongestContour(img=frame,type=ProcessType.CenterCoordinate,debug=True)
        else:
            x,y=camS.GetCenterByMatchTemplet(method=matchMethod)
            if len(xposData)>1:
                if abs(x-xposData[-1])>20:
                    continue
            if x==-1:
                break
        if not f.writable():
            print("File is occupied!Check access!")
        timeRecode=timer.TimePast()
        f.write(",".join([str(round(i,2)) for i in(x,y,timeRecode)])+"\n")
        # xposData.append(x)
        # timeData.append(timeRecode)
        # plt.plot(np.array(xposData),np.array(timeData))
        # plt.draw()
        k = cv2.waitKey(int(1000 / camS.getFPS()))
        if k == 27:
            break

    camS.releasCam()
    cv2.destroyAllWindows()
    f.close()
if __name__ == '__main__':
    runRecordData(3)