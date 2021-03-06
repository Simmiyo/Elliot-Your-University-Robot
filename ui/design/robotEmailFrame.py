# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'robotEmailFrame.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_emailFrame(object):
    def setupUi(self, emailFrame):
        emailFrame.setObjectName("emailFrame")
        emailFrame.resize(868, 509)
        self.gridLayout = QtWidgets.QGridLayout(emailFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.refrshTeachersButton = QtWidgets.QPushButton(emailFrame)
        self.refrshTeachersButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.refrshTeachersButton.setStyleSheet("background-color: rgb(255, 64, 77);")
        self.refrshTeachersButton.setObjectName("refrshTeachersButton")
        self.horizontalLayout.addWidget(self.refrshTeachersButton)
        self.attachmentsButton = QtWidgets.QPushButton(emailFrame)
        self.attachmentsButton.setStyleSheet("background-color: rgb(255, 64, 77);")
        self.attachmentsButton.setObjectName("attachmentsButton")
        self.horizontalLayout.addWidget(self.attachmentsButton)
        self.sendButton = QtWidgets.QPushButton(emailFrame)
        self.sendButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.sendButton.setStyleSheet("background-color: rgb(255, 64, 77);")
        self.sendButton.setObjectName("sendButton")
        self.horizontalLayout.addWidget(self.sendButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.browseBar = QtWidgets.QHBoxLayout()
        self.browseBar.setObjectName("browseBar")
        self.browseLabel = QtWidgets.QLabel(emailFrame)
        self.browseLabel.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";\n"
"color: rgb(179, 0, 2);")
        self.browseLabel.setObjectName("browseLabel")
        self.browseBar.addWidget(self.browseLabel)
        self.browseInput = QtWidgets.QLineEdit(emailFrame)
        self.browseInput.setStyleSheet("background-color:rgb(255, 255, 255);\n"
"border: 2px solid red; ")
        self.browseInput.setObjectName("browseInput")
        self.browseBar.addWidget(self.browseInput)
        self.verticalLayout.addLayout(self.browseBar)
        self.teachersListView = QtWidgets.QListView(emailFrame)
        self.teachersListView.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 2px solid red; ")
        self.teachersListView.setObjectName("teachersListView")
        self.verticalLayout.addWidget(self.teachersListView)
        self.gridLayout.addLayout(self.verticalLayout, 1, 2, 1, 1)
        self.emailCompose = QtWidgets.QVBoxLayout()
        self.emailCompose.setObjectName("emailCompose")
        self.subjectLabel = QtWidgets.QLabel(emailFrame)
        self.subjectLabel.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";\n"
"color: rgb(179, 0, 2);")
        self.subjectLabel.setObjectName("subjectLabel")
        self.emailCompose.addWidget(self.subjectLabel)
        self.subjectInput = QtWidgets.QLineEdit(emailFrame)
        self.subjectInput.setStyleSheet("background-color:rgb(255, 255, 255);\n"
"border: 2px solid red; ")
        self.subjectInput.setObjectName("subjectInput")
        self.emailCompose.addWidget(self.subjectInput)
        self.bodyLabel = QtWidgets.QLabel(emailFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bodyLabel.sizePolicy().hasHeightForWidth())
        self.bodyLabel.setSizePolicy(sizePolicy)
        self.bodyLabel.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";\n"
"color: rgb(179, 0, 2);")
        self.bodyLabel.setObjectName("bodyLabel")
        self.emailCompose.addWidget(self.bodyLabel)
        self.bodyInput = QtWidgets.QTextEdit(emailFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bodyInput.sizePolicy().hasHeightForWidth())
        self.bodyInput.setSizePolicy(sizePolicy)
        self.bodyInput.setStyleSheet("background-color:rgb(255, 255, 255);\n"
"border: 2px solid red; ")
        self.bodyInput.setObjectName("bodyInput")
        self.emailCompose.addWidget(self.bodyInput)
        self.gridLayout.addLayout(self.emailCompose, 1, 0, 1, 1)
        self.emailTeacherLabel = QtWidgets.QLabel(emailFrame)
        self.emailTeacherLabel.setObjectName("emailTeacherLabel")
        self.gridLayout.addWidget(self.emailTeacherLabel, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(emailFrame)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 1, 1, 1)

        self.retranslateUi(emailFrame)
        QtCore.QMetaObject.connectSlotsByName(emailFrame)

    def retranslateUi(self, emailFrame):
        _translate = QtCore.QCoreApplication.translate
        emailFrame.setWindowTitle(_translate("emailFrame", "Frame"))
        self.refrshTeachersButton.setText(_translate("emailFrame", "Refresh"))
        self.attachmentsButton.setText(_translate("emailFrame", "Attachments"))
        self.sendButton.setText(_translate("emailFrame", "Send"))
        self.browseLabel.setText(_translate("emailFrame", "Browse:"))
        self.subjectLabel.setText(_translate("emailFrame", "<html><head/><body><p>Introduce a title for your problem as mail subject:</p></body></html>"))
        self.bodyLabel.setText(_translate("emailFrame", "<html><head/><body><p>Introduce here the text describing the problem </p><p>you want to adress to a teacher:</p></body></html>"))
        self.emailTeacherLabel.setText(_translate("emailFrame", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; color:#cb2d45;\">E-mail a Teacher</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    emailFrame = QtWidgets.QFrame()
    ui = Ui_emailFrame()
    ui.setupUi(emailFrame)
    emailFrame.show()
    sys.exit(app.exec_())
