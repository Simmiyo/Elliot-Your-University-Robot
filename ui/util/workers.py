import datetime
import io
import json
import time
from os.path import abspath
from subprocess import Popen, PIPE, CREATE_NO_WINDOW

import requests
from PyQt5 import QtCore

from ui.util.logging_utils import log_exception
from ui.util.robots import getRobotPath


class RefreshStudentInfoWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal(bool)

    def __init__(self, userId=None, token=None):
        super(RefreshStudentInfoWorker, self).__init__()
        self._userId = userId
        self._token = token

    def run(self):
        try:
            headers = {'content-type': 'application/json', 'Authorization': f"Bearer {self._token}"}
            response = requests.get('http://localhost:3000/users/' + self._userId, headers=headers)
            if response.status_code == 200:
                data = json.loads(response.content.decode('utf-8'))
                data.update({'EmailAddress': data['email']})
                # metoda update pe dictionar primeste alt dictionar si il modifica pe cel obiect astfel:
                # daca cheia exista deja in dictionarul obiect, ii atribuie valoarea din dict param
                # daca cheia nu exista in disct ob, o adauga cu tot cu valoare din dict param
                try:
                    del data['id']
                    del data['email']
                    del data['password']
                    del data['cycle']
                    del data['faculty']
                    del data['registrationNumber']
                    del data['finished']
                    del data['gradesId']
                except KeyError:
                    pass
                with io.open('./data/StudentDataJSON.json', 'w', encoding='utf-8') as jFile:
                    json.dump(data, jFile, ensure_ascii=False)
                self.finished.emit(True)
            else:
                self.finished.emit(False)
        except Exception as e:
            log_exception(e)
            self.finished.emit(False)


class GetGradesWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal(str)

    def __init__(self, gradesId=None, cycle=None, year=None, sem=None, token=None):
        super(GetGradesWorker, self).__init__()
        self._gradesId = gradesId
        self.cycle = cycle
        self.year = year
        self.sem = sem
        self._token = token

    def run(self):
        if self._gradesId is None:     # iau gradesId daca e prima data cand intru pe note:
            with open('./data/StudentDataJSON.json', 'r', encoding='utf-8') as jFile:
                student = json.load(jFile)

            # cauta in baza de date, in tabelul cu relatii, dupa numele studenutului (relations?userName)
            # cerere get, intoarce o lista de dictionare ce contin datele cerute (de la usernameul dat)
            response = requests.get('http://localhost:3000/relations?userName=' + student['Surname'] + "-"
                                    + student['FirstName'])
            self._gradesId = json.loads(response.content.decode('utf-8'))[0]['gradesId']
            # [0] i.e. iau primul element al listei de dictionare (va fi doar unul oricum) & val din dict la cheia grId

        # zona comuna (indiferent daca e sau nu prima oara)
        headers = {'content-type': 'application/json', 'Authorization': f"Bearer {self._token}"}
        response = requests.get('http://localhost:3000/grades/' + str(self._gradesId), headers=headers)
        gradesJson = json.loads(response.content.decode('utf-8'))
        try:
            del gradesJson['id']
            del gradesJson['userId']
        except KeyError:
            pass

        if self.cycle:
            gradesData, nonZeroGrades = [], []
            for year in gradesJson[self.cycle]:
                if year["Year"] == self.year:
                    for elem in year["Semester " + self.sem]:
                        if elem['Grade'] != 0:
                            nonZeroGrades.append((elem['Grade'], elem['Credits']))    # calcul medii
                            gradesData.append(elem)     # afisare detaliata sit scol
                    break

            avgGrade = sum([g[0] for g in nonZeroGrades]) / len(nonZeroGrades)
            weightGrade = sum(g[0] * g[1] for g in nonZeroGrades) / sum([g[1] for g in nonZeroGrades])
            returnPacket = json.dumps({'data': gradesData, 'id': self._gradesId, 'avg': avgGrade, 'weight': weightGrade})
            self.finished.emit(returnPacket)
        else:
            returnPacket = json.dumps({'data': gradesJson, 'id': self._gradesId})
            self.finished.emit(returnPacket)


class GetMoodleCoursesList(QtCore.QObject):
    finished = QtCore.pyqtSignal(int)

    def __init__(self, csvStore: str, token=None, tokenPass=None, tStore=None):
        super(GetMoodleCoursesList, self).__init__()
        self._token = token
        self._tokenPass = tokenPass
        self.tStore = tStore
        self.csvStore = csvStore

    def run(self):
        try:
            with open('./data/StudentDataJSON.json', 'r', encoding='utf-8') as jFile:
                username = json.load(jFile)['EmailAddress']
            # command = [f".\\util\\moodle-api-request.exe", "-type refresh", f"-uname {username}", f"-cfile {self.csvStore}",
            #            f"-log {abspath(r'./logs/go.log')}"]
            logFile = r'"{}"'.format(abspath('./logs/go.log'))
            if self._token is None:    # token salvat (criptat) si dau comanda cu calea fisierului sau si parola
                # primul executabil
                # command += [f"-tfile {self.tStore}", f"-tpass {self._tokenPass}"]
                command = f".\\util\\moodle-api-request.exe -type refresh -tfile {self.tStore} -tpass {self._tokenPass} " \
                          f"-uname {username} -cfile {self.csvStore} -log {logFile}"
            else:    # tokenul este cunoscut (extras recent) si dau comanda direct cu tokenul
                # command += [f"-tval {self._token}"]
                command = f"./util/moodle-api-request.exe -type refresh -tval {self._token} -uname {username} " \
                          f"-cfile {self.csvStore} -log {logFile}"
            print(command)
            returnCode = Popen(command, stdout=PIPE, stderr=PIPE, shell=True).wait()
            # stdout, stderr = returnCode.communicate()
            # print(stdout.decode('utf-8'))
            # print(stderr.decode('utf-8'))
            # print(returnCode.returncode)
            # executabilul returneaza codul 0 daca totul a mers bine, 3 daca parola e gresita si alte numere pt alte sit
            self.finished.emit(returnCode)
        except Exception as e:
            log_exception(e)
            self.finished.emit(returnCode)


class SignalTokenExpire(QtCore.QObject):    # clasa workerilor care trimit semnal dupa trecerea timpului param
    finished = QtCore.pyqtSignal()

    def __init__(self, tokenExpTime=None):
        super(SignalTokenExpire, self).__init__()    # constructor baza QObject
        self.tokenExpTime = tokenExpTime

    # odata pornit, workerul doarme timpul param si apoi emite finished
    def run(self):
        time.sleep(self.tokenExpTime)
        self.finished.emit()


class CallUipathRobotWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal(bool)

    def __init__(self, args: dict):
        super(CallUipathRobotWorker, self).__init__()
        self._args = args

    def run(self):
        robotPath = r'"{}"'.format(getRobotPath())
        robotFile = r'"{}"'.format(abspath(r".\uipath\Main.xaml"))
        robotCommand = "cmd /c " + robotPath + " execute --file " + robotFile + " --input " + "\"" + str(self._args) + \
                       "\""     # comanda scrisa in command line
        print(robotCommand)
        # PIPE teava intre procese (fizic e un fisier special creat de os)
        robot = Popen(robotCommand, stdout=PIPE, stderr=PIPE, creationflags=CREATE_NO_WINDOW)    # creez proces extern
        stdout, stderr = robot.communicate()    # activez proces extern
        if stderr:
            print("Robot Error: ", stderr.decode('utf-8'))
            err = stderr.decode('utf-8')
            with open('./logs/uipath.log', 'a', encoding='utf-8') as logFile:
                logFile.write(f" {datetime.datetime.now()} - {err} \n")
        if stdout:
            print("Robot Output: " + stdout.decode('utf-8'))
            out = json.loads(stdout.decode('utf-8'))['robotSuccess']
            self.finished.emit(out)
        else:
            self.finished.emit(False)
