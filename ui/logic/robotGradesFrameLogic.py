import json

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFrame, QHeaderView

from ui.design.robotGradesFrame import Ui_gradesFrame
from ui.util.logging_utils import log_exception
from ui.util.models import GradesTableModel
from ui.util.workers import GetGradesWorker


class GradesFrameLogic(QFrame, Ui_gradesFrame):
    changeWindowSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent, securityToken):
        super(GradesFrameLogic, self).__init__(parent)
        self.parent = parent
        self.setupUi(parent)
        self._securityToken = securityToken
        self.gradesId = None
        self.avgGrade = None
        self.weightGrade = None
        self.model = None
        self.gradesStructure = {}

        self.gradesView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.gradesView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.gradesView.resizeRowsToContents()
        self.gradesView.resizeColumnsToContents()

        self.setState(False)

        try:
            self.getGrades(first='first')
        except Exception as e:
            log_exception(e)

        self.refreshButton.clicked.connect(self.getGrades)

    def setState(self, state: bool):
        self.refreshButton.setEnabled(state)
        self.cycleComboBox.setEnabled(state)
        self.yearComboBox.setEnabled(state)
        self.semesterComboBox.setEnabled(state)
        if not state:
            self.parent.setCursor(QtCore.Qt.WaitCursor)
        else:
            self.parent.setCursor(QtCore.Qt.ArrowCursor)

    def fillContents(self, returnPacket: str):  # fct doar pt prima vizita a procesului Grades
        # dupa ce umple si seteaza valorile selectorilor ciclu-an-sem, se comporta ca workerul pt vizite ulterioare

        returnPacket = json.loads(returnPacket)
        gradesJson = returnPacket['data']
        self.gradesId = returnPacket['id']

        lastCycle = None
        for key in gradesJson.keys():
            self.cycleComboBox.addItem(key)
            self.gradesStructure[key] = {}
            lastCycle = key
            for elem in gradesJson[key]:
                self.gradesStructure[key][elem["Year"]] = []
                if len(elem["Semester I"]) > 0:
                    self.gradesStructure[key][elem["Year"]].append("I")
                if len(elem["Semester II"]) > 0:
                    self.gradesStructure[key][elem["Year"]].append("II")

        lastCycleIndex = self.cycleComboBox.findText(lastCycle, QtCore.Qt.MatchFixedString)
        self.cycleComboBox.setCurrentIndex(lastCycleIndex)

        lastYear = None
        for year in self.gradesStructure[lastCycle].keys():
            self.yearComboBox.addItem(year)
            lastYear = year
        lastYearIndex = self.yearComboBox.findText(lastYear, QtCore.Qt.MatchFixedString)
        self.yearComboBox.setCurrentIndex(lastYearIndex)

        for sem in self.gradesStructure[lastCycle][lastYear]:
            self.semesterComboBox.addItem(sem)
        lastSemIndex = self.yearComboBox.findText(self.gradesStructure[lastCycle][lastYear][-1],
                                                  QtCore.Qt.MatchFixedString)
        self.semesterComboBox.setCurrentIndex(lastSemIndex)

        self.cycleComboBox.currentTextChanged.connect(self.getGrades)
        self.yearComboBox.currentTextChanged.connect(self.getGrades)
        self.semesterComboBox.currentTextChanged.connect(self.getGrades)

        gradesData, nonZeroGrades = [], []
        for elem in gradesJson[lastCycle][-1]["Semester " + self.gradesStructure[lastCycle][lastYear][-1]]:
            if elem['Grade'] != 0:
                nonZeroGrades.append((elem['Grade'], elem['Credits']))
                gradesData.append(elem)

        avgGrade = sum([g[0] for g in nonZeroGrades]) / len(nonZeroGrades)
        weightGrade = sum(g[0] * g[1] for g in nonZeroGrades) / sum([g[1] for g in nonZeroGrades])
        returnPacket = json.dumps({'data': gradesData, 'id': self.gradesId, 'avg': avgGrade, 'weight': weightGrade})

        self.renderGradesView(returnPacket)

    def renderGradesView(self, data: str):
        data = json.loads(data)
        self.model = GradesTableModel(data['data'])
        self.gradesView.setModel(self.model)
        self.gradesId = data['id']
        self.avgGrade = data['avg']
        self.weightGrade = data['weight']
        self.averageGradeLabel.setText(
            f"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Average Grade: {self.avgGrade: .2f}</span></p></body></html>")
        self.weightedGradeLabel.setText(
            f"<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Weighted Grade: {self.weightGrade: .2f}</span></p></body></html>")
        self.setState(True)

    def getGrades(self, first='first'):
        self.setState(False)
        try:
            self.thread = QtCore.QThread()
            if first != 'first':
                cycle = self.cycleComboBox.currentText()
                year = self.yearComboBox.currentText()
                sem = self.semesterComboBox.currentText()
                self.worker = GetGradesWorker(self.gradesId, cycle, year, sem, self._securityToken)
                self.worker.finished.connect(self.renderGradesView)
            else:
                self.worker = GetGradesWorker(token=self._securityToken)
                self.worker.finished.connect(self.fillContents)

            self.worker.moveToThread(self.thread)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)

            self.thread.started.connect(self.worker.run)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()
        except Exception as e:
            log_exception(e)
