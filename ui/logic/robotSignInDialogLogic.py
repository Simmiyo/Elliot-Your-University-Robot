import json
import jwt

import requests
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox

from ui.design.robotSingInDialog import Ui_SignInDialog
from ui.util.logging_utils import log_exception


class SignInDialogLogic(QDialog, Ui_SignInDialog):

    def __init__(self, parent):
        super(SignInDialogLogic, self).__init__(parent)
        self.parent = parent     # parent = scheletul paginii
        self.setupUi(parent)
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)    # parola tastata nu apare in clar
        # _numeVar sugereaza variabila privata in Python (desi nu e efectiv privata ca in C++ -
        # nu are nevoie de get set)
        self._token = ""
        self._userId = ''
        self.tokenExpTime = None

        # Qt functioneaza pe principiul semnale si sloturi (evenimentul si rezultatul lui)
        # clicked e semnal, handleLogic (metoda de mai jos) e slot
        self.signinButton.clicked.connect(self.handleLogin)
        self.cancelButton.clicked.connect(self.reject)

    def setTokenValue(self, value):
        self._token = value

    def setUserIdValue(self, value):
        self._userId = value

    def getTokenValue(self):
        return self._token

    def getUserIdValue(self):
        return self._userId

    def getTokenExpTime(self):
        return self.tokenExpTime

    # de la scheletul de QDialog (pt login)
    def reject(self):
        self.parent.reject()

    def accept(self):
        self.parent.accept()

    def exec_(self) -> int:
        return self.parent.exec_()

    def handleLogin(self):
        try:
            self.signinButton.setEnabled(False)    # blocare butoane pana se proceseaza raspunsul userului
            self.cancelButton.setEnabled(False)
            # logare cum o fac manual in powershell (cu toate datele de acolo, gen contentType)
            packet = {'email': self.emailEdit.text(), 'password': self.passwordEdit.text()}
            headers = {'content-type': 'application/json'}
            response = requests.post('http://localhost:3000/login/', json=packet, headers=headers)
            if response.status_code == 200:    # 200 = raspuns de acceptare clasic la http requests
                # dictionar cu cheie "accessToken" si valoare tokenul in string (din bytes)
                self.setTokenValue(json.loads(response.content.decode('utf-8'))['accessToken'])
                headerToken = jwt.decode(self._token, options={"verify_signature": False})
                self.tokenExpTime = headerToken['exp'] - headerToken['iat']  # exp, iat, sub -> componente payload token
                self.setUserIdValue(headerToken['sub'])
                self.accept()
            else:
                _ = QMessageBox.warning(self, 'Error!', 'Wrong user or password!')
                self.signinButton.setEnabled(True)   # deblocare butoane ca sa poti introduce iar user pass
                self.cancelButton.setEnabled(True)
        except Exception as e:    # e.g. nu i pornit serverul
            self.signinButton.setEnabled(True)
            self.cancelButton.setEnabled(True)
            _ = QMessageBox.critical(self, "Error!", "We could not connect to the server!")
            log_exception(e)
