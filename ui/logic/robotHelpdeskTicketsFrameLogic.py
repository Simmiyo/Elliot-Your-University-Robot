from PyQt5 import QtCore
from PyQt5.QtWidgets import QFrame, QDialog, QMessageBox

from ui.design.robotHelpdeskTicketsFrame import Ui_helpDeskFrame
from ui.logic.robotAttachementsDialogLogic import AttachDialogLogic
from ui.util.frameTypes import *
from ui.util.logging_utils import log_exception
from ui.util.workers import CallUipathRobotWorker


class HelpdeskTicketsFrameLogic(QFrame, Ui_helpDeskFrame):
    changeWindowSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        QFrame.__init__(self)
        self.parent = parent
        self.setupUi(parent)
        self.attachments = []

        self.oldTicketsButton.clicked.connect(lambda _: self.changeWindowSignal.emit(OLD_TICKETS))
        self.finishButton.clicked.connect(self.sendNewTicket)
        self.attachButton.clicked.connect(self.openAttachments)

    def setState(self, state: bool):
        self.attachButton.setEnabled(state)
        self.finishButton.setEnabled(state)
        self.oldTicketsButton.setEnabled(state)
        self.subjectInput.setEnabled(state)
        self.newTicketTextBox.setEnabled(state)
        if not state:
            self.parent.setCursor(QtCore.Qt.WaitCursor)
        else:
            self.parent.setCursor(QtCore.Qt.ArrowCursor)

    def ticketState(self, returnCode):
        if returnCode:
            _ = QMessageBox.information(self, "Success!", "The ticket was successfully sent!")
        else:
            _ = QMessageBox.warning(self, "Error!", "The ticket could not be sent!")
        self.setState(True)

    def sendNewTicket(self):
        ticketName = self.subjectInput.text()
        if ticketName == "":
            self.setState(False)
            _ = QMessageBox.warning(self, "No ticket name was given!", "You must name your ticket!")
            self.setState(True)
        else:
            ticketMessage = self.newTicketTextBox.toPlainText()
            if ticketMessage == "":
                self.setState(False)
                _ = QMessageBox.warning(self, "No ticket message was given!", "You must explain the problem on your "
                                                                              "own!")
                self.setState(True)
            else:
                self.setState(False)
                robotArgs = {"robotType": "helpDesk",
                             "helpType": "new",
                             "ticketName": ticketName,
                             "ticketBody": ticketMessage,
                             "attachments": ";".join(self.attachments)}
                try:
                    self.thread = QtCore.QThread()
                    self.worker = CallUipathRobotWorker(robotArgs)
                    self.worker.moveToThread(self.thread)

                    self.thread.started.connect(self.worker.run)
                    self.worker.finished.connect(self.thread.quit)
                    self.worker.finished.connect(self.ticketState)
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
