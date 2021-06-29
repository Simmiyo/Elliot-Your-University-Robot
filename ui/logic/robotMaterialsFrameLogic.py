import csv
import json
from os.path import abspath
from pathlib import Path
from subprocess import PIPE, Popen, CREATE_NO_WINDOW

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QFrame, QMessageBox

from ui.design.robotMaterialsFrame import Ui_materialsFrame
from ui.logic.robotAskTokenPasswordDialogLogic import AskTokenPassLogic
from ui.util.logging_utils import log_exception
from ui.util.robots import getRobotPath
from ui.util.workers import CallUipathRobotWorker, GetMoodleCoursesList


class MaterialsFrameLogic(QFrame, Ui_materialsFrame):
    changeWindowSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        QFrame.__init__(self)
        self.parent = parent
        self.setupUi(parent)

        self.coursesProxyModel = QtCore.QSortFilterProxyModel()
        self.coursesModel = QStandardItemModel()

        self.renderCoursesList(0)

        self.refreshButton.clicked.connect(lambda _: self.refreshCourses(""))
        self.filterLineEdit.textChanged.connect(self.coursesFilter)
        self.getButton.clicked.connect(self.getMaterials)
        self.choosePlatformComboBox.currentTextChanged.connect(lambda _: self.renderCoursesList(0))

    def setState(self, state: bool):
        self.refreshButton.setEnabled(state)
        self.getButton.setEnabled(state)
        self.filterLineEdit.setEnabled(state)
        self.choosePlatformComboBox.setEnabled(state)
        self.coursesView.setEnabled(state)
        if not state:
            self.parent.setCursor(QtCore.Qt.WaitCursor)
        else:
            self.parent.setCursor(QtCore.Qt.ArrowCursor)

    def getToken(self):
        robotCommand = "cmd /c " + getRobotPath() + " execute --file " + r".\uipath\Main.xaml " + \
                       r"--input " + "\"" + str({"robotType": "materials-extra", "platform": "moodle",
                                                 "tokenFile": r'"{}"'.format(abspath(r'.\data\token.txt'))})
        process = Popen(robotCommand, stdout=PIPE, stderr=PIPE, creationflags=CREATE_NO_WINDOW)
        stdout, stderr = process.communicate()
        if len(stderr.decode("utf-8")) == 0:
            token = json.loads(stdout.decode('utf-8', 'ignore'))['extractedToken']
            try:
                self.thread = QtCore.QThread()
                self.worker = GetMoodleCoursesList(r'"{}"'.format(abspath(r'.\data\coursesMoodle.csv')), token)
                self.worker.moveToThread(self.thread)

                self.thread.started.connect(self.worker.run)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.renderCoursesList)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)

                self.thread.start()
            except Exception as e:
                log_exception(e)

    # fct strict pt afisarea csvurilor deja memorate
    def renderCoursesList(self, needsRefresh):  # needsRefresh = semnalul emis de worker (returnCode de la primul exec)
        if needsRefresh == 0:
            try:
                platform = self.choosePlatformComboBox.currentText()
                if platform == "Moodle":
                    if not Path('./data/coursesMoodle.csv').is_file():
                        _ = QMessageBox.warning(self, "No Moodle courses file found!",
                                                "I could not find any list of courses!" +
                                                "Let's extract it now!")
                        self.refreshCourses("")
                    csvFile = './data/coursesMoodle.csv'
                else:
                    if not Path('./data/coursesTeams.csv').is_file():
                        _ = QMessageBox.warning(self, "No Teams courses file found!",
                                                "I could not find any list of courses!" +
                                                "Let's extract it now!")
                        self.refreshCourses("")
                    csvFile = './data/coursesTeams.csv'
                self.coursesProxyModel = QtCore.QSortFilterProxyModel()
                self.coursesModel = QStandardItemModel()
                with open(csvFile, newline='\n', encoding="utf8") as csvfile:
                    courses = csv.reader(csvfile, delimiter=',', quotechar='"')
                    for ind, row in enumerate(courses):
                        if ind != 0:
                            self.coursesModel.appendRow(QStandardItem(row[0]))
                self.coursesProxyModel.setSourceModel(self.coursesModel)
                self.coursesView.setModel(self.coursesProxyModel)
                self.setState(True)
            except Exception as e:
                log_exception(e)
                self.refreshCourses(tryText="")
        elif needsRefresh == 3:
            self.refreshCourses(tryText="Wrong Password! Try Again!")
        elif needsRefresh != 0:
            _ = QMessageBox.critical(self, "Unexpected problems with Moodle Unibuc!", "I experienced certain problems "
                                                                                      "while interacting with the "
                                                                                      "Moodle Unibuc API.")
            self.setState(True)

    def coursesFilter(self, filterText):
        filterRegex = QtCore.QRegExp(filterText,
                                     QtCore.Qt.CaseInsensitive,
                                     QtCore.QRegExp.RegExp
                                     )
        self.coursesProxyModel.setFilterRegExp(filterRegex)

    def refreshState(self, returnCode):
        if returnCode:
            _ = QMessageBox.information(self, "Success!", "The courses' list was successfully refreshed!")
            self.renderCoursesList(0)
        else:
            _ = QMessageBox.critical(self, "Unexpected problems with UiPath robot!",
                                     "I experienced certain problems while working with the UiPath" +
                                     "robots. Check the logs for more details.")
        self.setState(True)

    def refreshCourses(self, tryText: str):
        self.setState(False)
        platform = self.choosePlatformComboBox.currentText()
        if platform == "Moodle":
            if not Path('./data/token.txt').is_file():
                _ = QMessageBox.warning(self, "No token found!",
                                        "I could not find any encrypted Moodle security token! " +
                                        "So I must extract it!")
                self.getToken()
            else:
                AskPass = QtWidgets.QDialog()
                askUi = AskTokenPassLogic(AskPass, tryText)
                if askUi.exec_() == QtWidgets.QDialog.Accepted:  # s-a apasat submit
                    tokenPass = askUi.getPassword()
                    try:
                        self.thread = QtCore.QThread()
                        csvFile = r'"{}"'.format(abspath(r'.\data\coursesMoodle.csv'))
                        tokenFile = r'"{}"'.format(abspath(r'.\data\token.txt'))
                        self.worker = GetMoodleCoursesList(csvFile, None, tokenPass,
                                                           tokenFile)
                        self.worker.moveToThread(self.thread)

                        self.thread.started.connect(self.worker.run)
                        self.worker.finished.connect(self.thread.quit)
                        self.worker.finished.connect(self.renderCoursesList)
                        self.worker.finished.connect(self.worker.deleteLater)
                        self.thread.finished.connect(self.thread.deleteLater)

                        self.thread.start()
                    except Exception as e:
                        log_exception(e)
                elif askUi.forgotState:
                    self.getToken()
                else:
                    self.setState(True)
        else:
            robotArgs = {"robotType": "materials-extra", "platform": "teams",
                         "coursesFilePath": r'"{}"'.format(abspath(r'.\data\coursesTeams.csv'))}
            try:
                self.thread = QtCore.QThread()
                self.worker = CallUipathRobotWorker(robotArgs)
                self.worker.moveToThread(self.thread)

                self.thread.started.connect(self.worker.run)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.refreshState)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)

                self.thread.start()
            except Exception as e:
                log_exception(e)

    def getResults(self, returnCode):
        if not returnCode:
            _ = QMessageBox.critical(self, "Error!", "I experienced certain problems with the UiPath robots. Check "
                                                     "the logs for more details.")
        else:
            _ = QMessageBox.information(self, "Success!", "The materials were successfully extracted!")
        self.setState(True)

    def getMaterials(self):
        self.setState(False)
        selectedIndexes = self.coursesView.selectedIndexes()
        if not selectedIndexes:
            _ = QMessageBox.warning(self, "No course selected!", "Please select the course you want me to extract "
                                                                 "materials for!")
            self.setState(True)
        else:
            courseName = self.coursesProxyModel.itemData(selectedIndexes[0])[QtCore.Qt.DisplayRole]
            platform = self.choosePlatformComboBox.currentText()
            destinationPath = ""
            tokenFile = ""
            if platform == "Moodle":
                destinationPath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Please select destination folder!')
                tokenFile = r'"{}"'.format(abspath(r".\data\token.txt"))
                coursesFile = r'"{}"'.format(abspath(r".\data\coursesMoodle.csv"))
                courseName = r'"{}"'.format(courseName)
            else:
                coursesFile = r'"{}"'.format(abspath(r".\data\coursesTeams.csv"))
            if platform != 'Moodle' or destinationPath != "":
                robotArgs = {'robotType': 'get-materials', 'platform': platform, 'tokenFile': tokenFile,
                             'courseName': courseName, 'coursesFile': coursesFile,
                             'materialsDestination': destinationPath}
                try:
                    self.thread = QtCore.QThread()
                    self.worker = CallUipathRobotWorker(robotArgs)
                    self.worker.moveToThread(self.thread)

                    self.thread.started.connect(self.worker.run)
                    self.worker.finished.connect(self.thread.quit)
                    self.worker.finished.connect(self.getResults)
                    self.worker.finished.connect(self.worker.deleteLater)
                    self.thread.finished.connect(self.thread.deleteLater)

                    self.thread.start()
                except Exception as e:
                    print(e)
