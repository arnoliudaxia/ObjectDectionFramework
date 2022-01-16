import math
import time

# ===MathAndPhysic ===
def signal(intput):
    if intput >= 0:
        return 1
    if intput < 0:
        return -1


def angleCal(x, y):
    if x != 0 and y != 0:
        return math.atan(x / y) * 180 / math.pi


def Time2Length(time):
    return time ** 2 * 9.886 / (4 * math.pi ** 2)


def fixFunction(inputv):
    return inputv - math.log(10, inputv / 10) * 8.5

# ===Python Util===
class Timer:

    def __init__(self):
        self.clock=time.time()

    def Update(self):
        step = time.time() - self.clock
        print(f"Time step : {step}; FPS:{int(1.0/step)}")
        self.clock = time.time()
    def TimePast(self):
        return time.time()-self.clock