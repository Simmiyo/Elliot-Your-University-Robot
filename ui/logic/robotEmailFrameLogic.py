import csv
import json
from os.path import abspath
from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QFrame, QDialog, QMessageBox

from ui.design.robotEmailFrame import Ui_emailFrame
from ui.logic.robotAttachementsDialogLogic import AttachDialogLogic
from ui.util.logging_utils import log_exception
from ui.util.workers import CallUipathRobotWorker


class TeacherItem(QStandardItem):
    _EmailRole = QtCore.Qt.UserRole + 1   # rol custom (creat de mine prin +1 la un rol nefolosit de Qt)

    def __init__(self, parent=None, name=None, email=None):
        super(TeacherItem, self).__init__(parent)
        # setData, setText metode ale QStandardItem
        self.setData(email, TeacherItem._EmailRole)
        self.setText(name)


class EmailFrameLogic(QFrame, Ui_emailFrame):
    changeWindowSignal = QtCore.pyqtSignal(str)

    dummyMail = "simona.pop@my.fmi.unibuc.ro"

    def __init__(self, parent):
        QFrame.__init__(self)
        self.parent = parent
        self.setupUi(parent)
        self.attachments = []
        self.teachersProxyModel = QtCore.QSortFilterProxyModel()   # proxy = model special pt browse
        self.teachersModel = QStandardItemModel

        self.renderTeachersList()

        self.attachmentsButton.clicked.connect(self.openAttachments)
        self.browseInput.textChanged.connect(self.teachersFilter)    # la fiecare caract schimbat in browse bar -> tF
        self.refrshTeachersButton.clicked.connect(self.refreshTeachers)
        self.sendButton.clicked.connect(self.sendEmail)

    def setState(self, state: bool):
        self.refrshTeachersButton.setEnabled(state)
        self.sendButton.setEnabled(state)
        self.attachmentsButton.setEnabled(state)
        self.browseInput.setEnabled(state)
        self.bodyInput.setEnabled(state)
        self.subjectInput.setEnabled(state)
        if not state:
            self.parent.setCursor(QtCore.Qt.WaitCursor)
        else:
            self.parent.setCursor(QtCore.Qt.ArrowCursor)

    def teachersFilter(self, filterText):
        filterRegex = QtCore.QRegExp(filterText,
                                     QtCore.Qt.CaseInsensitive,
                                     QtCore.QRegExp.RegExp
                                     )
        self.teachersProxyModel.setFilterRegExp(filterRegex)

    def renderTeachersList(self):
        self.teachersProxyModel = QtCore.QSortFilterProxyModel()
        self.teachersModel = QStandardItemModel()
        if Path('./data/DepMate.csv').is_file() and Path('./data/DepInfo.csv').is_file():
            try:
                with open('./data/DepMate.csv', newline='\n', encoding="utf-8") as csvFile:
                    teachers = csv.reader(csvFile, delimiter=',', quotechar='"')
                    for ind, item in enumerate(teachers):
                        if ind != 0:
                            self.teachersModel.appendRow(TeacherItem(name=item[0], email=item[1]))
                with open('./data/DepInfo.csv', newline='\n', encoding="utf-8") as csvFile:
                    teachers = csv.reader(csvFile, delimiter=',', quotechar='"')
                    for ind, item in enumerate(teachers):
                        if ind != 0:
                            self.teachersModel.appendRow(TeacherItem(name=item[0], email=item[1]))
                self.teachersProxyModel.setSourceModel(self.teachersModel)
                self.teachersListView.setModel(self.teachersProxyModel)
                self.setState(True)
            except Exception as e:
                log_exception(e)
                self.refreshTeachers()
        else:
            self.refreshTeachers()

    def teachersState(self, returnCode: bool):
        if returnCode:
            _ = QMessageBox.information(self, "Success!", "The teachers' email addresses were successfully extracted!")
            self.renderTeachersList()
        else:
            resp = QMessageBox.warning(self, "Error!", "The teachers' email addresses could not be extracted due to "
                                                       "certain errors! Do you want to try again?",
                                       buttons=QMessageBox.Yes | QMessageBox.No)
            if resp == QMessageBox.Yes:
                self.refreshTeachers()
            else:
                self.setState(True)

    def refreshTeachers(self):
        self.setState(False)
        robotArgs = {"robotType": "refresh-teachers",
                     "mathTeachersStorePath": r'"{}"'.format(abspath(r'.\data\DepMate.csv')),
                     "infoTeachersStorePath": r'"{}"'.format(abspath(r'.\data\DepInfo.csv'))}
        try:
            self.thread = QtCore.QThread()
            self.worker = CallUipathRobotWorker(robotArgs)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.teachersState)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()
        except Exception as e:
            log_exception(e)

    def emailState(self, returnCode):
        if returnCode:
            _ = QMessageBox.information(self, "Success!", "The email was sent successfully!")
        else:
            _ = QMessageBox.warning(self, "Error!", "The email could not be sent!")
        self.sendButton.setEnabled(True)

    def sendEmail(self):
        emailSubject = self.subjectInput.text()
        if emailSubject == "":
            self.setState(False)
            _ = QMessageBox.warning(self, "No subject was given!", "I need a subject for the email!")
            self.setState(True)
        else:
            emailText = self.bodyInput.toPlainText()
            if emailText == "":
                self.setState(False)
                _ = QMessageBox.warning(self, "No mail body was given!", "I need a text body for the email!")
                self.setState(True)
            else:
                selectedTeacher = self.teachersListView.selectedIndexes()
                if not selectedTeacher:
                    self.setState(False)
                    _ = QMessageBox.warning(self, "No teacher was chosen!", "You must select a teacher!")
                    self.setState(True)
                else:
                    self.sendButton.setEnabled(False)
                    with open('./data/StudentDataJSON.json', 'r', encoding='utf-8') as jFile:
                        studentEmail = json.load(jFile)['EmailAddress']
                    teacherEmailAddress = selectedTeacher[0].data(TeacherItem._EmailRole)
                    robotArgs = {"robotType": "send-teacher-email",
                                 "recipientAddress": self.dummyMail,  # teacherEmailAddress
                                 "studentEmail": studentEmail,
                                 "emailSubject": emailSubject,
                                 "emailBody": emailText,
                                 "attachments": ";".join(self.attachments)}
                    try:
                        self.thread = QtCore.QThread()

                        self.worker = CallUipathRobotWorker(robotArgs)
                        self.worker.moveToThread(self.thread)

                        self.thread.started.connect(self.worker.run)
                        self.worker.finished.connect(self.thread.quit)
                        self.worker.finished.connect(self.emailState)
                        self.worker.finished.connect(self.worker.deleteLater)
                        self.thread.finished.connect(self.thread.deleteLater)

                        self.thread.start()
                    except Exception as e:
                        log_exception(e)

    def openAttachments(self):
        try:
            dialog = QDialog()
            uiAttach = AttachDialogLogic(dialog, files=self.attachments)
            _ = uiAttach.exec_()
            self.attachments = uiAttach.getFiles()
        except Exception as e:
            log_exception(e)
