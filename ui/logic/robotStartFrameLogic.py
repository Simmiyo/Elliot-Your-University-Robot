from PyQt5 import QtCore
from PyQt5.QtWidgets import QFrame

from ui.design.robotStartFrame import Ui_startFrame
from ui.util.frameTypes import *


class StartFrameLogic(QFrame, Ui_startFrame):    # mostenire schelet si design facut de mine in Qt
    changeWindowSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        QFrame.__init__(self)
        self.parent = parent
        self.setupUi(parent)    # fct din design care cere scheletul ca sa faca designul de care e nevoie
        # metoda connect vrea neaparat obiect de tip functie (de asta fac cu lambda expresii)
        self.documentsButton.clicked.connect(lambda _: self.changeWindowSignal.emit(PAPERWORK))
        self.gethelpButton.clicked.connect(lambda _: self.changeWindowSignal.emit(HELP))
        self.coursesButton.clicked.connect(lambda _: self.changeWindowSignal.emit(COURSES))
