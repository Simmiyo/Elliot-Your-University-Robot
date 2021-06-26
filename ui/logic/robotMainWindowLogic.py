import io
import json

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMainWindow, QFrame, QAction, QMessageBox, QApplication, QDialog

from ui.design.robotMainWindow import Ui_MainWindow
from ui.logic.robotCoursesFrameLogic import CoursesFrameLogic
from ui.logic.robotEmailFrameLogic import EmailFrameLogic
from ui.logic.robotGradesFrameLogic import GradesFrameLogic
from ui.logic.robotHelpFrameLogic import HelpFrameLogic
from ui.logic.robotHelpdeskOldTicketsFrameLogic import HelpdeskOldTicketsFrameLogic
from ui.logic.robotHelpdeskTicketsFrameLogic import HelpdeskTicketsFrameLogic
from ui.logic.robotMaterialsFrameLogic import MaterialsFrameLogic
from ui.logic.robotPaperworkFrameLogic import PaperworkFrameLogic
from ui.logic.robotSignInDialogLogic import SignInDialogLogic
from ui.logic.robotStartFrameLogic import StartFrameLogic
from ui.util.avatarImageMaker import maskImage
from ui.util.frameTypes import *
from ui.util.logging_utils import log_exception
from ui.util.workers import RefreshStudentInfoWorker, SignalTokenExpire


class MainWindowLogic(QMainWindow, Ui_MainWindow):
    def __init__(self, securityToken: str, userId: str, tokenExpTime=None, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        self._securityToken = securityToken
        self._userId = userId
        self.tokenExpTime = tokenExpTime

        # fac logo din panglica rotund
        self.verticalLayout_2.removeWidget(self.avatarLabel)
        imgdata = open('./images/robo.png', 'rb').read()
        pixmap = maskImage(imgdata, imgtype='png', size=150)
        self.avatarLabel.setPixmap(pixmap)
        self.verticalLayout_2.insertWidget(0, self.avatarLabel, 0, Qt.AlignCenter)

        # initializare cu start frame
        self.horizontalLayout_2.removeWidget(self.mainFrame)
        self.frame = QFrame()
        self.horizontalLayout_2.addWidget(self.frame)
        self.changeMainFrame(START)
        self.currentFrame = START
        self.mainFrame = None

        # creez actiunea back
        self.menuBack.setGeometry(0, 0, 50, 50)
        self.backAction = QAction('Back', self)
        self.backAction.setShortcut('BackSpace')
        self.menuBack.addAction(self.backAction)
        self.menuBack.triggered[QAction].connect(self.goBack)

        # creez actiunea refresh info
        self.editButton.clicked.connect(self.refreshInfo)

        #
        self.tokenTime()
        self.refreshInfo()

    def tokenTime(self):
        try:
            self.thread_1 = QtCore.QThread()  # creez thread
            self.worker_1 = SignalTokenExpire(self.tokenExpTime)  # creez worker care trimite semnal la expirare timp
            self.worker_1.finished.connect(self.reLogin)  # la expirare timp merg la login

            self.worker_1.moveToThread(self.thread_1)  # pun workerul pe thread
            self.worker_1.finished.connect(self.thread_1.quit)  # workerul pune threadul sa-si termine executia
            self.worker_1.finished.connect(self.worker_1.deleteLater)  # workerul va fi distrus candva dupa ce a term

            self.thread_1.started.connect(self.worker_1.run)  # cand incepe executia threadului, pornesc si workerul
            self.thread_1.finished.connect(self.thread_1.deleteLater)  # threadul va fi distrus candva dupa ce a term

            self.thread_1.start()
        except Exception as e:
            log_exception(e)

    def reLogin(self):
        try:
            _ = QMessageBox.warning(self, "The security token expired!", "You will need to sing in again!")
            signInDialog = QDialog()
            signInUi = SignInDialogLogic(signInDialog)

            if signInUi.exec_() == QDialog.Accepted:
                self._securityToken = signInUi.getTokenValue()
                self._userId = signInUi.getUserIdValue()
                self.tokenExpTime = signInUi.getTokenExpTime()
                self.tokenTime()
            else:
                QApplication.quit()
        except Exception as e:
            log_exception(e)

    def goBack(self):
        if self.currentFrame == START:
            pass
        if self.currentFrame in [PAPERWORK, HELP, COURSES]:
            self.changeMainFrame(START)
        if self.currentFrame in [HELPDESK, EMAIL]:
            self.changeMainFrame(HELP)
        if self.currentFrame in [MATERIALS, GRADES]:
            self.changeMainFrame(COURSES)
        if self.currentFrame == OLD_TICKETS:
            self.changeMainFrame(HELPDESK)

    def changeMainFrame(self, frameType: str):
        self.horizontalLayout_2.removeWidget(self.frame)
        self.frame = QFrame()
        if frameType == START:
            self.mainFrame = StartFrameLogic(self.frame)
        elif frameType == PAPERWORK:
            self.mainFrame = PaperworkFrameLogic(self.frame)
        elif frameType == HELP:
            self.mainFrame = HelpFrameLogic(self.frame)
        elif frameType == COURSES:
            self.mainFrame = CoursesFrameLogic(self.frame)
        elif frameType == EMAIL:
            self.mainFrame = EmailFrameLogic(self.frame)
        elif frameType == HELPDESK:
            self.mainFrame = HelpdeskTicketsFrameLogic(self.frame)
        elif frameType == OLD_TICKETS:
            self.mainFrame = HelpdeskOldTicketsFrameLogic(self.frame)
        elif frameType == MATERIALS:
            self.mainFrame = MaterialsFrameLogic(self.frame)
        elif frameType == GRADES:
            self.mainFrame = GradesFrameLogic(self.frame, self._securityToken)
        self.currentFrame = frameType
        self.mainFrame.changeWindowSignal.connect(lambda frame: self.changeMainFrame(frame))
        self.horizontalLayout_2.addWidget(self.frame)
        self.show()

    def renderRibbon(self):  # json deja actualizat, asta e pasul in care se rescrie panglica in fct de json
        with io.open('./data/StudentDataJSON.json', 'r', encoding='utf-8') as jFile:
            studentData = json.load(jFile)
        self.hellotextLabel.setText(
            f"<html><head/><body><p align=\"center\">"
            f"<span style=\" font-size:11pt;\">Hello, </span><span style=\" font-size:11pt; font-weight:600; "
            f"font-style:italic;\">{studentData['FirstName']} "
            f"</span><span style=\" font-size:11pt;\">!</span></p><p align=\"center\"><span style=\" "
            f"font-size:11pt;\">I\'m "
            f"</span><span style=\" font-size:11pt; font-weight:600;\">ELLIOT</span><span style=\" font-size:11pt;\">, "
            f"your university robot!</span></p></body></html>")
        self.nameLabel.setText(
            f"<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">{studentData['Surname']} "
            f"{studentData['FirstName']}</span></p></body></html>")
        self.emailLabel.setText(
            f"<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">{studentData['EmailAddress']}"
            f"</span></p></body></html>")
        self.phoneLabel.setText(
            f"<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">{studentData['Phone']}"
            f"</span></p></body></html>")
        self.groupLabel.setText(
            f"<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">Grupa {studentData['Class']}"
            f"</span></p></body></html>")
        self.yearLabel.setText(
            f"<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">Anul {studentData['Year']}"
            f"</span></p></body></html>")
        self.domainLabel.setText(
            f"<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">Domeniul {studentData['Domain']}"
            f"</span></p></body></html>")
        self.specialityLabel.setText(
            f"<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">"
            f"Specializarea {studentData['Specialization']}</span></p></body></html>")

    def refreshState(self, response: bool):
        if response:
            self.renderRibbon()    # modific panglica cu noile date din json
        else:
            _ = QMessageBox.critical(self, "Error!",
                                    "We could not refresh your info due to certain problems with the server!")
        self.editButton.setEnabled(True)
        self.ribbonFrame.setCursor(QtCore.Qt.ArrowCursor)
        # while QApplication.overrideCursor() is not None:
        #     QApplication.restoreOverrideCursor()

    def refreshInfo(self):
        self.editButton.setEnabled(False)
        self.ribbonFrame.setCursor(QtCore.Qt.WaitCursor)
        # QApplication.setOverrideCursor(QCursor(QtCore.Qt.WaitCursor))
        try:
            self.thread = QtCore.QThread()
            self.worker = RefreshStudentInfoWorker(self._userId, self._securityToken)
            self.worker.finished.connect(self.refreshState)

            self.worker.moveToThread(self.thread)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)

            self.thread.started.connect(self.worker.run)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()
        except Exception as e:
            log_exception(e)
