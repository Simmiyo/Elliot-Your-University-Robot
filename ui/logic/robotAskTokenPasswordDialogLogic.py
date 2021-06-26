from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog

from ui.design.robotAskTokenPasswordDialog import Ui_AksPassworDialog


class AskTokenPassLogic(QDialog, Ui_AksPassworDialog):

    def __init__(self, parent, tryText):
        super(AskTokenPassLogic, self).__init__(parent)
        self.parent = parent
        self.setupUi(parent)
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)    # ascunde parola
        self.submitButton.clicked.connect(self.accept)
        self.forgotButton.clicked.connect(self.reject)
        self._password = ""
        self.forgotState = False
        self.tryAgainLabel.setText(
            f"<html><head/><body><p align=\"center\"><span style=\" font-size:9pt; color:#f30000;\">{tryText}</span></p></body></html>")

    def getPassword(self):
        return self._password

    def accept(self):
        self._password = self.passwordEdit.text()
        self.parent.accept()

    def reject(self):
        self.forgotState = True
        self.parent.reject()

    def exec_(self) -> int:
        return self.parent.exec_()
