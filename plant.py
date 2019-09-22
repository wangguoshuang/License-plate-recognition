
# -*- coding: UTF-8 -*-
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from hyperlpr import *
import numpy as np
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
# from PyQt5.QtCore import QDate, QTime, QDateTime, Qt


#画框函数
fontC = ImageFont.truetype(r"C:\Users\cy\PycharmProjects\untitled/Font/platech.ttf", 55, 0)
# fontC2 = ImageFont.truetype(r"C:\Users\cy\PycharmProjects\untitled\Font/platech.ttf", 125, 0)
def drawRectBox(image, rect, addText):
    cv2.rectangle(image, (int(rect[0]), int(rect[1])), (int(rect[2]), int(rect[3])), (34, 250, 21), 10,
                  cv2.LINE_AA)
    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img)
    draw.text((int(rect[0] ), int(rect[1] - 80)), addText.encode("utf-8").decode("utf-8"), (2, 235,233 ), font=fontC)
    imagex = np.array(img)
    return imagex


def drawRectBox_img(image, rect, addText):
    cv2.rectangle(image, (int(rect[0]), int(rect[1])), (int(rect[2]), int(rect[3])), (34, 250, 21), 10,
                  cv2.LINE_AA)
    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img)
    draw.text((int(rect[0]-30 ), int(rect[1] - 70)), addText.encode("utf-8").decode("utf-8"), (2, 235,233 ), font=fontC)
    imagex = np.array(img)
    return imagex

class WorkThread(QThread):
    add_item = pyqtSignal(QImage)
    add_item2 = pyqtSignal(str)
    add_item3 = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(QThread, self).__init__(*args, **kwargs)
        self.num = 0

    def run(self):
        cap = cv2.VideoCapture(0)
        # cap.set(3, 960)
        # cap.set(4, 720)
        while (1):

            ret, frame = cap.read()
            # show a frame
            if (any(HyperLPR_PlateRecogntion(frame))):
                for pstr, confidence, rect in HyperLPR_PlateRecogntion(frame):
                    image = drawRectBox(frame, rect, pstr)
                    self.add_item2.emit(pstr)
                    if confidence > 0.9 :
                        print(f"车牌号:{pstr}")
                        print(f"可靠度:{confidence}")
                    show = cv2.resize(image, (640, 480))  # 把读到的帧的大小重新设置为 640x480
            else:
                show = cv2.resize(frame, (640, 480))  # 把读到的帧的大小重新设置为 640x480
            show2 = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
            showImage = QtGui.QImage(show2.data, show2.shape[1], show2.shape[0],
                                     QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式

            # cv2.imshow("capture", frame)
            self.add_item.emit(showImage)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)

        self.set_ui()
        self.slot_init()
        self.__flag_work = 0
        self.x = 0
        self.count = 0


    def set_ui(self):

        self.setMinimumSize(800,600)
        self.setMaximumSize(800,600)
        #
        # palette = QPalette()
        # palette.setBrush(QPalette.Background, QBrush(QPixmap(r'C:\Users\cy\Desktop\new plate\bj0.png')))
        # self.setPalette(palette)

        self.setObjectName('Ui_MainWindow')
        self.setWindowTitle(u'车牌识别')
#显示车牌
        self.ll = QLabel(self)
        self.cy = QLineEdit(self)

        self.cy.setText('欢迎验收')
        # self.cy.setStyleSheet("background:transparent;border-width:0;border-style:outset;color:yellow")
        self.cy.setFont(QFont("Roman times", 12, QFont.Bold))
        self.ll.setText("车牌号：")
        # self.ll.setStyleSheet("color:white")
        self.ll.setFont(QFont("楷体",13,QFont.Bold))
        self.cy.move(590, 10)
        self.ll.move(500, 10)
#显示时间

        self.time = QLabel(self)
        self.time.setFont(QFont("楷体", 13, QFont.Bold))
        self.time.setText("时间")
        self.time2 = QLineEdit(self)

        self.time2.setStyleSheet("background:transparent;border-width:0;border-style:outset;color:rgb(10,20,10)")
        # self.time.setStyleSheet("color:white")
        self.time2.setFont(QFont("Roman times", 13, QFont.Bold))
        self.time2.move(60, 10)
        self.time.move(10, 10)


        self.__layout_main = QtWidgets.QHBoxLayout()
        self.__layout_fun_button = QtWidgets.QVBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()

        self.button_open_camera = QtWidgets.QPushButton(u'实时视频识别')
        self.button_open_img = QtWidgets.QPushButton(u'选图识别')
        self.button_close = QtWidgets.QPushButton(u'退出')
        self.button_more = QtWidgets.QPushButton(u'更多')


        # Button 的颜色修改
        button_color = [self.button_open_camera,self.button_open_img, self.button_close,self.button_more]
        for i in range(4):
            button_color[i].setStyleSheet("QPushButton{color:rgb(68,68,51)}"
                                          "QPushButton:hover{color:yellow}"
                                          "QPushButton{background-color:rgb(68,221,204)}"
                                          "QPushButton{border:55px}"
                                          "QPushButton{font: bold}"
                                          "QPushButton{border-radius:20px}"
                                          "QPushButton{padding:18px 4px}")




        # move()方法移动窗口在屏幕上的位置到x = 300，y = 300坐标。
        self.move(600, 200)

        # 信息显示
        self.label_show_camera = QtWidgets.QLabel()
        self.label_move = QtWidgets.QLabel()
        self.label_move.setFixedSize(80, 0)

        self.label_show_camera.setFixedSize(720, 500)
        self.label_show_camera.setAutoFillBackground(False)

        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_open_img)
        self.__layout_fun_button.addWidget(self.button_close)
        self.__layout_fun_button.addWidget(self.button_more)

        self.__layout_fun_button.addWidget(self.label_move)

        self.__layout_main.addLayout(self.__layout_fun_button)
        self.__layout_main.addWidget(self.label_show_camera)

        self.setLayout(self.__layout_main)
        self.label_move.raise_()

        self.th1 = WorkThread()

        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.start()


    def slot_init(self):

        self.button_open_img.clicked.connect(self.button_open_img_click)
        self.button_close.clicked.connect(self.close)
        self.button_open_camera.clicked.connect(self.startTh1)
        self.button_more.clicked.connect(self.click_morebutton)
        self.th1.add_item.connect(self.show_camera)
        self.th1.add_item2.connect(self.show_Text)

    def startTh1(self):
        self.th1.start()
        self.cy.setText('Loading..')
        # self.cy.setStyleSheet("background:transparent;border-width:0;border-style:outset;color:rgb(10,10,10)")
        # self.cy.setFont(QFont("Roman times", 12, QFont.Bold))
        self.button_open_camera.setText(u'识别中')
        # self.tq2.setText(f + '元')

    def show_camera(self,showImage):

        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
    def show_Text(self,pstr):
        try:
            self.cy.setText(pstr[0]+pstr[1]+'-'+pstr[2]+pstr[3]+pstr[4]+pstr[5]+pstr[6])
            # self.cy.setStyleSheet("background:transparent;border-width:0;border-style:outset;color:rgb(100,200,100)")
            self.cy.setFont(QFont("Roman times", 12, QFont.Bold))
        except:
            print("溢出警告！！！")

    def button_open_img_click(self):
        self.button_open_img.setText(u'找图中')
        pic_path, _ = QFileDialog.getOpenFileName(self, '取一张图片', r'C:\Users\cy\Desktop\new plate', 'Image files(*.jpg *.gif *.png)')
        if pic_path:
            image = cv2.imread(pic_path)
            for pstr, confidence, rect in HyperLPR_PlateRecogntion(image):
                image2 = drawRectBox_img(image, rect, pstr)
                if confidence > 0.9:
                    self.cy.setText(pstr[0]+pstr[1]+'-'+pstr[2]+pstr[3]+pstr[4]+pstr[5]+pstr[6])
                    show = cv2.resize(image2, (720, 650))
                    show2 = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
                    showImage = QtGui.QImage(show2.data, show2.shape[1], show2.shape[0],
                                             QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
                    self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
                    self.button_open_img.setText(u'再来一张呗！')

    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cacel = QtWidgets.QPushButton()
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u"凉凉.jpg", u"确定吗！")
        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cacel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'我确定')
        cacel.setText(u'再挣扎一下')
        msg.setDetailedText('')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            event.accept()
    def click_morebutton(self):
        self.button_more.move(10,500)
        self.button_more.setText("")


    def showtime(self):
            time = QTime.currentTime()
            self.time2.setText(time.toString(Qt.DefaultLocaleLongDate))



if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(App.exec_())
