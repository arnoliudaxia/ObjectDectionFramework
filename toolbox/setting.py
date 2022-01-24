import numpy as np
import json,os

# noinspection SpellCheckingInspection
ColoriniURL= os.path.dirname(__file__)+r"\ini\color.ini"
# noinspection SpellCheckingInspection
MotioniniURL= os.path.dirname(__file__)+r"\ini\motion.ini"
CamerainiURL=os.path.dirname(__file__)+r"\ini\camera.ini"
def readColorIni():
    f = open(ColoriniURL, "r")
    inis=json.loads(f.readline())
    lower_red=np.array(inis["ColorBound"]["low"])
    upper_red=np.array(inis["ColorBound"]["high"])

    return lower_red,upper_red
def saveColorini(ColorBound):
    f = open(ColoriniURL, "r+")
    inis=json.loads(f.readline())
    inis["ColorBound"]["low"]=ColorBound[0]
    inis["ColorBound"]["high"]=ColorBound[1]

    f.seek(0)
    f.writelines(json.dumps(inis))
    f.close()
def readMotionIni():
    f = open(MotioniniURL, "r")
    inis=json.loads(f.readline())
    kernelSize=int(inis['kernelSize'])
    iterations=int(inis['iterations'])
    f.close()
    return kernelSize,iterations

def saveMotionini(kernelSize=-1,iterations=-1):
    f = open(MotioniniURL, "r+")
    inis = json.loads(f.readline())
    if kernelSize!=-1:
        inis['kernelSize'] = kernelSize
    if iterations!=-1:
        inis['iterations'] = iterations

    f.seek(0)
    f.writelines(json.dumps(inis))
    f.close()

def readCameraIni():
    f = open(CamerainiURL, "r")
    inis=json.loads(f.readline())
    url=str(inis['URL'])
    f.close()
    return url

def saveCameraIni(url):
    f = open(CamerainiURL, "r+")
    inis = json.loads(f.readline())
    inis["URL"]=url

    f.seek(0)
    f.writelines(json.dumps(inis))
    f.close()


if __name__ == "__main__":
    import sys,os
    sys.path.append(os.path.abspath(".."))
