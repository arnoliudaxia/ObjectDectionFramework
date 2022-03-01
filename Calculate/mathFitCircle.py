from sys import path

import numpy as np
import cv2
import matplotlib.pyplot as plt
import scipy.optimize as opt

def runMathFit(filepath):
    f = open(filepath, "r")
    data = f.readlines()
    f.close()
    points = []
    for datum in data:
        points.append([float(i) for i in datum.replace("\n", "").split(",")][:-1])
    data = np.array(points, dtype=np.float)

    trackImg = cv2.cvtColor(np.zeros((480, 640), dtype=np.uint8), cv2.COLOR_GRAY2BGR)
    for point in data.astype(np.int):
        pass#cv2.circle(trackImg, point, 1, (255, 255, 255))
    cv2.imshow("track", trackImg)


    rx = int(data.mean(axis=0)[0])#rx是所有点的中心线
    ry = int(data.mean(axis=0)[1])

    xs = np.linspace(ry, ry - 500, 500)
    y = [np.var(np.sqrt(np.sum((data - (rx, x)) ** 2, axis=1))) for x in xs]
    plt.plot(xs, y)
    plt.show()

    ry = opt.minimize(lambda x: np.nanstd(np.sqrt(np.sum((data - (rx, x[0])) ** 2, axis=1))), np.array([ry])).x[0]
    # ry = round(xs[np.argmin(y)])
    ry=round(ry)
    r = round(np.mean(np.sqrt(np.sum((data - (rx, ry)) ** 2, axis=1))))
    cv2.namedWindow('Result', cv2.WINDOW_AUTOSIZE)
    cv2.createTrackbar("Length(px)","Result",r,300,lambda x:1+1)
    print(f"R:{r}")
    cv2.circle(trackImg, (rx, ry), r, (0, 0, 255), 2)
    cv2.line(trackImg, (rx, 0), (rx, 470), (0, 0, 255), 2)
    cv2.imshow("Regression", trackImg)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
    return f"{r} px"


if __name__ == '__main__':
    runMathFit(r"..\data.txt")
