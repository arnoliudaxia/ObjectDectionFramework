import numpy as np
import json


iniURL=r"C:\Users\Arnoliu\PycharmProjects\opecvtry\toolbox\color.ini"
def readColorIni():
    f = open(iniURL, "r")
    inis=json.loads(f.readline())
    lower_red=np.array(inis["ColorBound"]["low"])
    upper_red=np.array(inis["ColorBound"]["high"])

    return lower_red,upper_red
def saveColorini(ColorBound):
    f = open(iniURL, "r+")
    inis=json.loads(f.readline())
    inis["ColorBound"]["low"]=ColorBound[0]
    inis["ColorBound"]["high"]=ColorBound[1]

    f.seek(0)
    f.writelines(json.dumps(inis))
    f.close()
