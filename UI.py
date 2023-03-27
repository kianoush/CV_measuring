# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPalette, QImage
import numpy

import cv2
import utlis
import imutils
import os
import datetime
#import PIL


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(788, 720)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 771, 681))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMouseTracking(True)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Img01.png"))
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("Img02.jpg"))
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton = QtWidgets.QPushButton(self.frame_3)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 28))
        self.pushButton.setMaximumSize(QtCore.QSize(16777215, 28))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icons/play-circle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(16, 16))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_3.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 28))
        self.pushButton_2.setMaximumSize(QtCore.QSize(16777215, 28))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Icons/download.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_3.addWidget(self.pushButton_2, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(532, 19, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.start_measuring) # type: ignore
        self.pushButton_2.clicked.connect(self.save_img) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.webcam = False
        self.save_image = False
        self.path = 'Img01.png'
        self.cap = cv2.VideoCapture(0)
        self.cap.set(10,160)
        self.cap.set(3,1920)
        self.cap.set(4,1080)
        self.scale = 3
        self.wP = 210 *self.scale
        self.hP= 297 *self.scale


    def start_measuring(self):
        """ This function turn on the camera"""
        self.webcam = True
        self.measureing()

    def measureing(self):

        """ This function obtain the image and recognize the object and measure it
        """
        run = True
        while run:
            if self.webcam:
                success, img = self.cap.read()
            else:
                img = cv2.imread(self.path)

            imgContours, conts = utlis.getContours(img, minArea=50000, filter=4)
            if len(conts) != 0:
                biggest = conts[0][2]
                # print(biggest)
                imgWarp = utlis.warpImg(img, biggest, self.wP, self.hP)
                imgContours2, conts2 = utlis.getContours(imgWarp,
                                                         minArea=2000, filter=4,
                                                         cThr=[50, 50], draw=False)
                if len(conts) != 0:
                    for obj in conts2:
                        cv2.polylines(imgContours2, [obj[2]], True, (200, 200, 0), 1)
                        nPoints = utlis.reorder(obj[2])
                        nW = round((utlis.findDis(nPoints[0][0] // self.scale, nPoints[1][0] // self.scale) / 10), 1)
                        nH = round((utlis.findDis(nPoints[0][0] // self.scale, nPoints[2][0] // self.scale) / 10), 1)
                        cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]),
                                        (nPoints[1][0][0], nPoints[1][0][1]),
                                        (200, 100, 255), 3, 8, 0, 0.05)
                        cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]),
                                        (nPoints[2][0][0], nPoints[2][0][1]),
                                        (200, 100, 255), 3, 8, 0, 0.05)
                        x, y, w, h = obj[3]
                        cv2.putText(imgContours2, '{}cm'.format(nW), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                    1.5,
                                    (200, 100, 255), 1)
                        cv2.putText(imgContours2, '{}cm'.format(nH), (x - 70, y + h // 2),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                                    (200, 100, 255), 1)
                self.update_measureWin(imgContours2)

            img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
            self.update(img)
            k = cv2.waitKey(0) & 0xFF
            if k == 27:  # close on ESC key
                cv2.destroyAllWindows()
                run = False


    def save_img(self):
        self.save_image = True


    def update(self, image):
        """ This function will take image input and resize it
            only for display purpose and convert it to QImage
            to set at the label.
        """
        self.tmp = image
        image = imutils.resize(image, width=550, height=550)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))

    def update_measureWin(self, image):
        """ This function will take image input and resize it
            only for display purpose and convert it to QImage
            to set at the label.
        """
        self.tmp01 = image
        image = imutils.resize(image, width=215, height=600)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.label_2.setPixmap(QtGui.QPixmap.fromImage(image))
        if self.save_image:
            try:
                os.mkdir('./Save_img/')
            except:
                pass

            filename1 = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            img_name = "opencv_frame_{}.png".format(filename1)
            cv2.imwrite('./Save_img/'+ img_name, frame)
            print("{} written!".format(img_name))
            self.save_image = False



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start measuring"))
        self.pushButton_2.setText(_translate("MainWindow", "Save"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
