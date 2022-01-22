import numpy as np
from sys import path
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.stats as stat
from toolbox.mathUtility import Time2Length

def runSignalProcess(filepath):
    f = open(filepath, "r")
    data = f.readlines()
    f.close()
    points = []
    for datum in data:
        points.append([float(i) for i in datum.replace("\n", "").split(",")])
    data = np.array(points, dtype=np.float)
    times=data[:,2]
    xs=data[:,0]
    plt.title("TimeDomin")
    plt.plot(times,xs)
    plt.show()
    peaks=sig.find_peaks(xs)
    average_time=stat.linregress(np.arange(len(peaks[0])),times[peaks[0]]).slope
    print(f"L is {Time2Length(average_time)} m.")
    return f"{Time2Length(average_time)} m"