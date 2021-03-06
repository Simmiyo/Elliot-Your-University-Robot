# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'robotStartFrame.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_startFrame(object):
    def setupUi(self, startFrame):
        startFrame.setObjectName("startFrame")
        startFrame.resize(798, 480)
        self.horizontalLayout = QtWidgets.QHBoxLayout(startFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.documentsFrame = QtWidgets.QFrame(startFrame)
        self.documentsFrame.setStyleSheet("background: transparent;")
        self.documentsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.documentsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.documentsFrame.setObjectName("documentsFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.documentsFrame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.documentsButton = QtWidgets.QPushButton(self.documentsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.documentsButton.sizePolicy().hasHeightForWidth())
        self.documentsButton.setSizePolicy(sizePolicy)
        self.documentsButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.documentsButton.setStyleSheet("QPushButton {\n"
"  background: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(51, 130, 173, 255), stop:1 rgba(255, 255, 255, 255));\n"
"  border-color: rgb(51, 130, 173);\n"
"  border-width: 3px;        \n"
"  border-style: solid;\n"
"  border-radius: 40px;\n"
"  margin:30px;\n"
"  padding:30px;\n"
"}")
        self.documentsButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/papers.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.documentsButton.setIcon(icon)
        self.documentsButton.setIconSize(QtCore.QSize(100, 100))
        self.documentsButton.setObjectName("documentsButton")
        self.verticalLayout_3.addWidget(self.documentsButton)
        self.paperworkLabel = QtWidgets.QLabel(self.documentsFrame)
        self.paperworkLabel.setObjectName("paperworkLabel")
        self.verticalLayout_3.addWidget(self.paperworkLabel)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.documentsFrame)
        self.gethelpFrame = QtWidgets.QFrame(startFrame)
        self.gethelpFrame.setStyleSheet("background: transparent;")
        self.gethelpFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.gethelpFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gethelpFrame.setObjectName("gethelpFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.gethelpFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.gethelpButton = QtWidgets.QPushButton(self.gethelpFrame)
        self.gethelpButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.gethelpButton.setStyleSheet("QPushButton {\n"
"  background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.119403 rgba(255, 0, 38, 255), stop:1 rgba(255, 255, 255, 255));\n"
"  border-color: rgb(203, 45, 69);\n"
"  border-width: 3px;        \n"
"  border-style: solid;\n"
"  border-radius: 40px;\n"
"  margin:30px;\n"
"  padding:30px;\n"
"}")
        self.gethelpButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.gethelpButton.setIcon(icon1)
        self.gethelpButton.setIconSize(QtCore.QSize(100, 100))
        self.gethelpButton.setObjectName("gethelpButton")
        self.verticalLayout_4.addWidget(self.gethelpButton)
        self.gethelpLabel = QtWidgets.QLabel(self.gethelpFrame)
        self.gethelpLabel.setObjectName("gethelpLabel")
        self.verticalLayout_4.addWidget(self.gethelpLabel)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.horizontalLayout.addWidget(self.gethelpFrame)
        self.coursesFrame = QtWidgets.QFrame(startFrame)
        self.coursesFrame.setStyleSheet("background: transparent;")
        self.coursesFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.coursesFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.coursesFrame.setObjectName("coursesFrame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.coursesFrame)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem4)
        self.coursesButton = QtWidgets.QPushButton(self.coursesFrame)
        self.coursesButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.coursesButton.setStyleSheet("QPushButton {\n"
"  background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.189055 rgba(144, 189, 0, 255), stop:0.900498 rgba(255, 255, 255, 255));\n"
"  border-color: rgb(144, 177, 36);\n"
"  border-width: 3px;        \n"
"  border-style: solid;\n"
"  border-radius: 40px;\n"
"  margin:30px;\n"
"  padding:30px;\n"
"}")
        self.coursesButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/grades-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.coursesButton.setIcon(icon2)
        self.coursesButton.setIconSize(QtCore.QSize(100, 100))
        self.coursesButton.setObjectName("coursesButton")
        self.verticalLayout_5.addWidget(self.coursesButton)
        self.coursesLabel = QtWidgets.QLabel(self.coursesFrame)
        self.coursesLabel.setObjectName("coursesLabel")
        self.verticalLayout_5.addWidget(self.coursesLabel)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem5)
        self.horizontalLayout.addWidget(self.coursesFrame)
        self.paperworkLabel.setBuddy(self.documentsButton)
        self.gethelpLabel.setBuddy(self.gethelpButton)
        self.coursesLabel.setBuddy(self.coursesButton)

        self.retranslateUi(startFrame)
        QtCore.QMetaObject.connectSlotsByName(startFrame)

    def retranslateUi(self, startFrame):
        _translate = QtCore.QCoreApplication.translate
        startFrame.setWindowTitle(_translate("startFrame", "Frame"))
        self.paperworkLabel.setText(_translate("startFrame", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#3382ad;\">Paperwork</span></p></body></html>"))
        self.gethelpLabel.setText(_translate("startFrame", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#cb2d45;\">Get Help</span></p></body></html>"))
        self.coursesLabel.setText(_translate("startFrame", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#90b124;\">Courses</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    startFrame = QtWidgets.QFrame()
    ui = Ui_startFrame()
    ui.setupUi(startFrame)
    startFrame.show()
    sys.exit(app.exec_())
