from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFrame

from ui.design.robotHelpFrame import Ui_helpFrame
from ui.util.frameTypes import *


class HelpFrameLogic(QFrame, Ui_helpFrame):
    changeWindowSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        QFrame.__init__(self)
        self.parent = parent
        self.setupUi(parent)
        self.emailButton.clicked.connect(lambda _: self.changeWindowSignal.emit(EMAIL))
        self.helpdeskButton.clicked.connect(lambda _: self.changeWindowSignal.emit(HELPDESK))
