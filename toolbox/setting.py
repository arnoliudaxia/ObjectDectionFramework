import numpy as np


iniURL=r"C:\Users\Arnoliu\PycharmProjects\opecvtry\task\Color\color.ini"
def readColorIni():
    lower_red = None
    upper_red = None
    f = open(iniURL, "r")
    inis=f.readlines()
    for ini in inis:
        ini = ini.split(" ")
        if(ini[0]=="color_bound"):
            icol = [int(i) for i in ini[1:]]
            lower_red = np.array(icol[0:3])
            upper_red = np.array(icol[3:])
    return lower_red,upper_red
def saveColorini(ColorBound):
    ColorBound[0]=[str(i) for i in ColorBound[0]]
    ColorBound[1]=[str(i) for i in ColorBound[1]]
    f = open(iniURL, "r+")
    inis = f.readlines()
    Towrite=[]
    for ini in inis:
        ini = ini.split(" ")
        if (ini[0] == "color_bound"):
            ini[1:4]=ColorBound[0]
            ini[4:]=ColorBound[1]
        ini=" ".join(ini)
        Towrite.append(ini)
    f.seek(0)
    f.writelines(Towrite)
    f.close()