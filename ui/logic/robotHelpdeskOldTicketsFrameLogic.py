from os.path import abspath
from pathlib import Path

import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFrame, QHeaderView, QMessageBox

from ui.design.robotHelpdeskOldTicketsFrame import Ui_oldTicketsFrame
from ui.util.logging_utils import log_exception
from ui.util.models import TicketsTableModel
from ui.util.workers import CallUipathRobotWorker


class HelpdeskOldTicketsFrameLogic(QFrame, Ui_oldTicketsFrame):
    changeWindowSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        QFrame.__init__(self)
        self.parent = parent
        self.setupUi(parent)

        self.openTicketsModel = None
        self.closedTicketsModel = None
        self.viewOpenTickets.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.viewClosedTickets.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.setState(False)
        self.renderTickets(0)
        self.tabTicketsWidget.currentChanged.connect(self.renderTickets)
        self.reloadButton.clicked.connect(self.refreshTickets)

    def setState(self, state: bool):
        self.reloadButton.setEnabled(state)
        self.tabTicketsWidget.setEnabled(state)
        self.viewOpenTickets.setEnabled(state)
        self.viewClosedTickets.setEnabled(state)
        if not state:
            self.parent.setCursor(QtCore.Qt.WaitCursor)
            self.tabTicketsWidget.setCursor(QtCore.Qt.WaitCursor)
        else:
            self.tabTicketsWidget.setCursor(QtCore.Qt.ArrowCursor)
            self.parent.setCursor(QtCore.Qt.ArrowCursor)

    def renderTickets(self, ticketsType: int):
        if ticketsType == 0:
            if Path('./data/OpenTickets.csv').is_file():
                try:
                    # citeste csv, intoarce tabel (data frame) in loc de simpla lista
                    openTickets = pd.read_csv('./data/OpenTickets.csv', encoding='utf-8')
                    self.openTicketsModel = TicketsTableModel(openTickets)
                    self.viewOpenTickets.setModel(self.openTicketsModel)
                    self.setState(True)
                except Exception as e:
                    log_exception(e)
                    self.refreshTickets()
            else:
                self.refreshTickets()
        else:
            if Path('./data/ClosedTickets.csv').is_file():
                try:
                    closedTickets = pd.read_csv('./data/ClosedTickets.csv', encoding='utf-8')
                    self.closedTicketsModel = TicketsTableModel(closedTickets)
                    self.viewClosedTickets.setModel(self.closedTicketsModel)
                    self.setState(True)
                except Exception as e:
                    log_exception(e)
                    self.refreshTickets()
            else:
                self.refreshTickets()

    def ticketState(self, returnCode):
        if returnCode:
            _ = QMessageBox.information(self, "Success!", "The tickets were successfully extracted!")
            self.renderTickets(0)
        else:
            _ = QMessageBox.warning(self, "Error!", "The tickets could not be extracted due to certain problems with "
                                                    "the UiPath robot!")
            self.setState(True)

    def refreshTickets(self):
        self.setState(False)
        robotArgs = {"robotType": "helpDesk",
                     "helpType": "check",
                     "openTicketsFile": r'"{}"'.format(abspath(r'.\data\OpenTickets.csv')),
                     "closedTicketsFile": r'"{}"'.format(abspath(r'.\data\ClosedTickets.csv'))}
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
