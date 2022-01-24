import os
import sys
sys.path.append(os.path.abspath(".."))
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication, QDesktopWidget, QMessageBox, QVBoxLayout, QLabel, QHBoxLayout,
                             QLineEdit, QComboBox, QTextBrowser, QFontDialog, QStyleFactory)
from PyQt5.QtGui import QFont
from QCandyUi import CandyWindow
from QCandyUi.CandyWindow import colorful
from ColorCailbrate import runColorConfigure
from findPen import runFindPen
import recordData
from Calculate import mathFitCircle,SignalProcess


def centerWindow(window:QWidget):
    # 获得窗口
    qr = window.frameGeometry()
    # 获得屏幕中心点
    cp = QDesktopWidget().availableGeometry().center()
    # 显示到屏幕中心
    qr.moveCenter(cp)
    window.move(qr.topLeft())
def tranfertoColor():
    global mainMenu
    global colorMenu
    mainMenu.hide()
    colorMenu.show()
def analyzeData(method:int,fill:QTextBrowser):
    res=-1
    if method==1:
        res=mathFitCircle.runMathFit(os.path.abspath('')+r"\data.txt")
    if method==2:
        res=SignalProcess.runSignalProcess(os.path.abspath('')+r"\data.txt")
    fill.clear()
    fill.append(str(res))


class MainMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 这种静态的方法设置一个用于显示工具提示的字体。我们使用10px滑体字体。
        QToolTip.setFont(QFont('SansSerif', 10))

        # 创建一个提示，我们称之为settooltip()方法。我们可以使用丰富的文本格式
        self.setToolTip('This is a <b>QWidget</b> widget')

        vbox=QVBoxLayout()

        # 颜色识别btn
        btn = QPushButton('颜色识别', self)
        btn.setObjectName("btnMenu")
        btn.setToolTip('提取图像中特定颜色区间的部分，适用于颜色鲜明的主题，与背景有较大的区分度')
        btn.clicked.connect(tranfertoColor)
        vbox.addWidget(btn)
        # btn.resize(btn.sizeHint())
        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 200)
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


        vbox=QVBoxLayout()
        vbox.addWidget(QLabel('First Step--Color configuration'))
        vbox.addWidget(QLabel('点击下面的按钮后会弹出一个配置窗口，需要调整参数使得黑白画面中白色部分刚好是物体本身。'))
        vbox.addWidget(QLabel('按Esc键不保存退出，按s键会保存配置文件到color.ini文件中'))
        vbox.addWidget(QLabel('Hint：一般来说先调低阈值，使得物体的图像显性完全即可。然后调整高阈值，将背景抹除。'))
        ColorConfigureBtn=QPushButton("Configure")
        ColorConfigureBtn.clicked.connect(runColorConfigure)
        vbox.addWidget(ColorConfigureBtn)
        vbox.addWidget(QLabel('Second Step--Dection Test'))
        vbox.addWidget(QLabel('点击下面的按钮后，如果参数正确，那么物体就会用红框框出'))
        vbox.addWidget(QLabel('按Esc键退出'))
        TestBtn = QPushButton("Test")
        TestBtn.clicked.connect(lambda :runFindPen(1))
        vbox.addWidget(TestBtn)
        vbox.addWidget(QLabel('Third Step--RecordData'))
        vbox.addWidget(QLabel('点击下面的按钮后，使用参数记录物体的轨迹与时间戳数据储存于data.txt'))
        vbox.addWidget(QLabel('按Esc键停止记录'))
        RecordBtn = QPushButton("Record")
        RecordBtn.clicked.connect(lambda :recordData.runRecordData(1))
        vbox.addWidget(RecordBtn)
        vbox.addWidget(QLabel('Fourth Step--Analyze Data'))
        vbox.addWidget(QLabel('读取data.txt中存储的数据，利用不同的数学物理方法求得绳长'))
        combox=QComboBox()
        combox.insertItem(0,"数学拟合")
        combox.insertItem(1,"信号处理")
        combox.setCurrentIndex(1)
        vbox.addWidget(combox)
        ResultField=QTextBrowser()
        # ResultField.setFont()
        AnalyzeBtn = QPushButton("Analyze")
        AnalyzeBtn.clicked.connect(lambda: analyzeData(combox.currentIndex()+1,ResultField))
        vbox.addWidget(AnalyzeBtn)
        vbox.addWidget(QLabel("R:"))
        vbox.addWidget(ResultField)

        self.setLayout(vbox)

app = QApplication(sys.argv)
css=open("stylesheets/flatwhite.css")
app.setStyleSheet(css.read())
css.close()
mainMenu = MainMenu()
colorMenu=ColorMenu()
sys.exit(app.exec_())

#主题美化：https://zhuanlan.zhihu.com/p/390192953；https://github.com/UN-GCPDS/qt-material;https://www.google.com.hk/search?q=qss样式分享&ie=utf-8&oe=utf-8