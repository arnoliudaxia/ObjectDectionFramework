import os
import sys
# 将本项目的主文件夹添加到path中（临时）
sys.path.append(os.path.abspath(os.path.dirname(__file__) + os.path.sep + ".."))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + os.path.sep + "."))


from toolbox.opencvFramework import CamerSystem
from toolbox.setting import *
import cv2

sys.path.append(os.path.abspath(""))
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QDesktopWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox,
                             QTextBrowser, QMessageBox)
from PyQt5.QtGui import QFont
from ColorCailbrate import runColorConfigure
from MotionCailbrate import runMotionCailbrate
from findPen import runFindPen
import recordData
from Calculate import mathFitCircle, SignalProcess


def centerWindow(window: QWidget):
    # 获得窗口
    qr = window.frameGeometry()
    # 获得屏幕中心点
    cp = QDesktopWidget().availableGeometry().center()
    # 显示到屏幕中心
    qr.moveCenter(cp)
    window.move(qr.topLeft())


def tranfertoMenu(MenuName):
    global mainMenu
    global colorMenu
    global motionMenu
    global matchMenu
    mainMenu.hide()
    if MenuName == "Main":
        colorMenu.hide()
        motionMenu.hide()
        matchMenu.hide()
        mainMenu.show()
    if MenuName == "Color":
        colorMenu.show()
    if MenuName == "Motion":
        motionMenu.show()
    if MenuName=="Match":
        matchMenu.show()


def analyzeData(method: int, fill: QTextBrowser):
    res = -1
    if method == 1:
        res = mathFitCircle.runMathFit(os.path.abspath('') + r"\data.txt")
    if method == 2:
        res = SignalProcess.runSignalProcess(os.path.abspath('') + r"\data.txt")
    fill.clear()
    fill.append(str(res))


def loadCamera(url: str):
    url = url.replace('"', '')
    CamerSystem.cameraMainURL = url
    saveCameraIni(url)
def checkSnip():
    global matchMenu
    isExist=True
    try:
        img=cv2.imread("obj.jpg")
        cv2.imshow("图片",img,)
    except:
        isExist=False

    if isExist:
        QMessageBox.information(matchMenu,"Message","截图已完成！")
    else:
        QMessageBox.ctitical(matchMenu,"错误","没有找到截图图片，确认本文件同目录下有obj.jpg文件")


class MainMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 这种静态的方法设置一个用于显示工具提示的字体。我们使用10px滑体字体。
        self.setFont(QFont('SansSerif', 10))

        vbox = QVBoxLayout()

        # 视频流URL
        QLabel("视频流地址", self)
        URLField = QLineEdit()
        URLField.setText(readCameraIni())
        URLField.textChanged[str].connect(loadCamera)
        vbox.addWidget(URLField)
        # 颜色识别btn
        Colorbtn = QPushButton('颜色识别', self)
        Colorbtn.setObjectName("btnMenu")
        Colorbtn.setToolTip('提取图像中特定颜色区间的部分，适用于颜色鲜明的主题，与背景有较大的区分度')
        Colorbtn.clicked.connect(lambda x: tranfertoMenu("Color"))
        vbox.addWidget(Colorbtn)
        # 运动检测btn
        MotionBtn = QPushButton('运动检测(KNN)', self)
        MotionBtn.setObjectName("btnMenu")
        MotionBtn.setToolTip('通过帧与帧之间的差分计算视频中远动的部分（光流法）.\n'
                             '注意目前主流的背景分割器有MOG，KNN和GMG,在此例中使用KNN的效果最好\n'
                             '在不稳定的环境下不建议Record太多数据，反而有反效果')
        MotionBtn.clicked.connect(lambda x: tranfertoMenu("Motion"))
        vbox.addWidget(MotionBtn)
        # 目标跟踪
        trackBtn = QPushButton('目标跟踪')
        trackBtn.setObjectName("btnMenu")
        trackBtn.setToolTip("可以注意到前面的MotionDection已经不是传统意义上的ObjectDection了\n"
                            "它已经使用了前后相关帧做分析，可以归类为目标跟踪算法\n"
                            "而然它又算不上真正的目标跟踪，从原理来说前后帧作差分（虽然不仅仅是差分）仅仅是为了导出图像的'速度场'\n"
                            "所以更贴切来说它应该是'动态目标检测'\n"
                            "真正的目标跟踪算法非常重要的一环是目标运动的估计，对图像滤波\n"
                            "最近正要过年，先不研究了，挖个坑先")

        vbox.addWidget(trackBtn)
        #模板匹配
        matchBtn= QPushButton('模板匹配')
        matchBtn.setObjectName("btnMenu")
        matchBtn.setToolTip("这种方法其实是最好理解的，就是如果有物体的图片，那么只需要将这个和视频里的每一帧做比对，最像（图片差最小）的就是物体在的地方\n"
                            "目前这个方法还需要滤波器消除毛刺，需要完善")
        matchBtn.clicked.connect(lambda x: tranfertoMenu("Match"))

        vbox.addWidget(matchBtn)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 352, 273)

        self.setWindowTitle('ObjectDetectionDemo')
        centerWindow(self)

        self.show()


# @colorful('blueGreen','ColorFilter')
class ColorMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 640, 573)
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setWindowTitle('ColorFilter')
        centerWindow(self)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('First Step--Color configuration'))
        vbox.addWidget(QLabel('点击下面的按钮后会弹出一个配置窗口，需要调整参数使得黑白画面中白色部分刚好是物体本身。'))
        vbox.addWidget(QLabel('按Esc键不保存退出，按s键会保存配置文件到color.ini文件中'))
        vbox.addWidget(QLabel('Hint：一般来说先调低阈值，使得物体的图像显性完全即可。然后调整高阈值，将背景抹除。'))
        ColorConfigureBtn = QPushButton("Configure")
        ColorConfigureBtn.clicked.connect(runColorConfigure)
        vbox.addWidget(ColorConfigureBtn)
        vbox.addWidget(QLabel('Second Step--Dection Test'))
        vbox.addWidget(QLabel('点击下面的按钮后，如果参数正确，那么物体就会用红框框出'))
        vbox.addWidget(QLabel('按Esc键退出'))
        TestBtn = QPushButton("Test")
        TestBtn.clicked.connect(lambda: runFindPen(1))
        vbox.addWidget(TestBtn)
        vbox.addWidget(QLabel('Third Step--RecordData'))
        vbox.addWidget(QLabel('点击下面的按钮后，使用参数记录物体的轨迹与时间戳数据储存于data.txt'))
        vbox.addWidget(QLabel('按Esc键停止记录'))
        RecordBtn = QPushButton("Record")
        RecordBtn.clicked.connect(lambda: recordData.runRecordData(1))
        vbox.addWidget(RecordBtn)
        vbox.addWidget(QLabel('Fourth Step--Analyze Data'))
        vbox.addWidget(QLabel('读取data.txt中存储的数据，利用不同的数学物理方法求得绳长'))
        combox = QComboBox()
        combox.insertItem(0, "数学拟合")
        combox.insertItem(1, "信号处理")
        combox.setCurrentIndex(1)
        vbox.addWidget(combox)
        ResultField = QTextBrowser()
        # ResultField.setFont()
        AnalyzeBtn = QPushButton("Analyze")
        AnalyzeBtn.clicked.connect(lambda: analyzeData(combox.currentIndex() + 1, ResultField))
        vbox.addWidget(AnalyzeBtn)
        vbox.addWidget(QLabel("R:"))
        vbox.addWidget(ResultField)
        # Return to MainMenu
        MenuBtn = QPushButton("←")
        MenuBtn.clicked.connect(lambda: tranfertoMenu("Main"))
        vbox.addWidget(MenuBtn)

        self.setLayout(vbox)


class MotionMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 640, 573)
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setWindowTitle('MotionDection')
        centerWindow(self)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('ConfigureKNN'))
        vbox.addWidget(QLabel('点击下面的按钮后，将调试KNN分割器参数，其中kernelsize和iteration可以动态调整，且会自动保存'))
        vbox.addWidget(QLabel('按Esc键结束'))
        ConfigureBtn = QPushButton("Configure")
        ConfigureBtn.clicked.connect(lambda: runMotionCailbrate())
        vbox.addWidget(ConfigureBtn)

        vbox.addWidget(QLabel('RecordData'))
        vbox.addWidget(QLabel('点击下面的按钮后，将使用KNN分割器检测目标'))
        vbox.addWidget(QLabel('按Esc键停止记录'))
        RecordBtn = QPushButton("Record")
        RecordBtn.clicked.connect(lambda: recordData.runRecordData(2))
        vbox.addWidget(RecordBtn)
        vbox.addWidget(QLabel('Analyze Data'))
        vbox.addWidget(QLabel('读取data.txt中存储的数据，利用不同的数学物理方法求得绳长'))
        combox = QComboBox()
        combox.insertItem(0, "数学拟合")
        combox.insertItem(1, "信号处理")
        combox.setCurrentIndex(1)
        vbox.addWidget(combox)
        ResultField = QTextBrowser()
        # ResultField.setFont()
        AnalyzeBtn = QPushButton("Analyze")
        AnalyzeBtn.clicked.connect(lambda: analyzeData(combox.currentIndex() + 1, ResultField))
        vbox.addWidget(AnalyzeBtn)
        vbox.addWidget(QLabel("R:"))
        vbox.addWidget(ResultField)
        # Return to MainMenu
        MenuBtn = QPushButton("←")
        MenuBtn.clicked.connect(lambda: tranfertoMenu("Main"))
        vbox.addWidget(MenuBtn)

        self.setLayout(vbox)

class MatchMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 640, 573)
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setWindowTitle('TempletMatch')
        centerWindow(self)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('Snip'))
        vbox.addWidget(QLabel('在开始之前，先截个物体的图片保存为obj.jpg，尽量只包含物体的最小图片\n'
                              '我肝不动了就不做截图功能了'))
        CheckBtn = QPushButton("Check")
        CheckBtn.setToolTip("点击我可以检查是否完成,正常的话还会显示截图")
        CheckBtn.clicked.connect(checkSnip)
        vbox.addWidget(CheckBtn)

        vbox.addWidget(QLabel('RecordData'))
        vbox.addWidget(QLabel('下面可以选择不同的匹配方法'))
        Matchcombox = QComboBox()
        Matchcombox.insertItem(0, "平方差匹配")
        Matchcombox.insertItem(1, "标准平方差匹配")
        Matchcombox.insertItem(2, "交叉相关匹配")
        Matchcombox.insertItem(3, "归一化交叉相关匹配 ")
        Matchcombox.insertItem(4, "相关系数匹配")
        Matchcombox.insertItem(5, "归一化相关系数匹配")
        vbox.addWidget(Matchcombox)
        vbox.addWidget(QLabel('按Esc键停止记录'))
        RecordBtn = QPushButton("Record")
        RecordBtn.clicked.connect(lambda: recordData.runRecordData(3, Matchcombox.currentIndex()))
        vbox.addWidget(RecordBtn)
        vbox.addWidget(QLabel('Analyze Data'))
        vbox.addWidget(QLabel('读取data.txt中存储的数据，利用不同的数学物理方法求得绳长'))
        combox = QComboBox()
        combox.insertItem(0, "数学拟合")
        combox.insertItem(1, "信号处理")
        combox.setCurrentIndex(1)
        vbox.addWidget(combox)
        ResultField = QTextBrowser()
        AnalyzeBtn = QPushButton("Analyze")
        AnalyzeBtn.clicked.connect(lambda: analyzeData(combox.currentIndex() + 1, ResultField))
        vbox.addWidget(AnalyzeBtn)
        vbox.addWidget(QLabel("R:"))
        vbox.addWidget(ResultField)
        # Return to MainMenu
        MenuBtn = QPushButton("←")
        MenuBtn.clicked.connect(lambda: tranfertoMenu("Main"))
        vbox.addWidget(MenuBtn)

        self.setLayout(vbox)
app = QApplication(sys.argv)
css = open("stylesheets/flatwhite.css")
app.setStyleSheet(css.read())
css.close()
mainMenu = MainMenu()
colorMenu = ColorMenu()
motionMenu = MotionMenu()
matchMenu=MatchMenu()
sys.exit(app.exec_())

# 主题美化：https://zhuanlan.zhihu.com/p/390192953；https://github.com/UN-GCPDS/qt-material;https://www.google.com.hk/search?q=qss样式分享&ie=utf-8&oe=utf-8
