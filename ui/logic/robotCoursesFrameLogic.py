from PyQt5 import QtCore
from PyQt5.QtWidgets import QFrame

from ui.design.robotCoursesFrame import Ui_coursesFrame
from ui.util.frameTypes import *


class CoursesFrameLogic(QFrame, Ui_coursesFrame):
    changeWindowSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        QFrame.__init__(self)
        self.parent = parent
        self.setupUi(parent)
        self.materialsButton.clicked.connect(lambda _: self.changeWindowSignal.emit(MATERIALS))
        self.gradesButton.clicked.connect(lambda _: self.changeWindowSignal.emit(GRADES))
