import json

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QFrame, QMessageBox, QApplication

from ui.design.robotPaperworkFrame import Ui_paperworkFrame
from ui.util.logging_utils import log_exception
from ui.util.workers import CallUipathRobotWorker
import os.path


class PaperworkFrameLogic(QFrame, Ui_paperworkFrame):
    changeWindowSignal = QtCore.pyqtSignal(str)

    needFill = ['Adeverință Cercetare Elaborare Licență', 'Cerere Aprobare Licență',
                'Declarație Autenticitate Lucrare Licență',
                'Fișă de Lichidare', 'Cerere de Echivalare']

    def __init__(self, parent):
        QFrame.__init__(self)
        self.parent = parent
        self.setupUi(parent)

        with open('./data/StudentDataJSON.json', 'r', encoding='utf-8') as jFile:
            self.studentEmail = json.load(jFile)['EmailAddress']

        self.requestDocButton.clicked.connect(self.requestDoc)
        self.sendDocButton.clicked.connect(self.sendDoc)

    def setState(self, state: bool):
        self.requestDocButton.setEnabled(state)
        self.sendDocButton.setEnabled(state)
        if not state:
            self.parent.setCursor(QtCore.Qt.WaitCursor)
        else:
            self.parent.setCursor(QtCore.Qt.ArrowCursor)

    def robotRequestState(self, returnCode: int):
        self.setState(True)
        if not returnCode:
            _ = QMessageBox.critical(self, "Problems with Uipath robot!",
                                    "We expecienced some unkown problem with the Uipath " +
                                    "robots. Check the logs for more details.")
        else:
            _ = QMessageBox.information(self, "Success!", "I successfully accomplished your command!")

    def sendDoc(self):
        self.setState(False)
        selected = self.toSentList.selectedIndexes()
        if selected:
            doc = self.toSentList.currentItem().text()
            ready = True
            if doc in self.needFill:
                docName = doc.replace(" ", "-") + "-template.docx"
                docPath = os.path.join(os.path.abspath(r".\data\templates"), docName)
                needsFill = "true"
            else:
                needsFill = "false"
                docPath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select the file you would like to send!')
                if not docPath:
                    _ = QMessageBox.warning(self, "No document file selected!",
                                            "You need to select a file document!")
                    ready = False
            if ready:
                robotArgs = {"robotType": "paperwork",
                             "requestType": "send",
                             "studentEmail": self.studentEmail,
                             'needsFill': needsFill,
                             'docName': doc,
                             'docPath': docPath}
                try:
                    self.thread = QtCore.QThread()

                    self.worker = CallUipathRobotWorker(robotArgs)
                    self.worker.moveToThread(self.thread)

                    self.thread.started.connect(self.worker.run)
                    self.worker.finished.connect(self.thread.quit)
                    self.worker.finished.connect(self.robotRequestState)
                    self.worker.finished.connect(self.worker.deleteLater)
                    self.thread.finished.connect(self.thread.deleteLater)

                    self.thread.start()
                except Exception as e:
                    log_exception(e)
            else:
                self.setState(True)
        else:
            _ = QMessageBox.warning(self, "No document selected!",
                                    "You need to select a document!")
            self.setState(True)

    def requestDoc(self):
        self.setState(False)
        selected = self.toRequestList.selectedIndexes()
        if selected:

            docType = self.toRequestList.currentItem().text()
            robotArgs = {"robotType": "paperwork",
                         "requestType": "request",
                         "studentEmail": self.studentEmail,
                         'docType': docType}
            try:
                self.thread = QtCore.QThread()

                self.worker = CallUipathRobotWorker(robotArgs)
                self.worker.moveToThread(self.thread)

                self.thread.started.connect(self.worker.run)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.robotRequestState)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)

                self.thread.start()
            except Exception as e:
                log_exception(e)
        else:
            _ = QMessageBox.warning(self, "No document selected!",
                                    "You need to select a document")
            self.setState(True)
