import typing

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QAbstractTableModel
from pathlib import Path


# modelele sunt necesare view-urilor


class FilesListModel(QtCore.QAbstractListModel):    # pt attachments
    def __init__(self, files=None, *args, **kwargs):
        super(FilesListModel, self).__init__(*args, **kwargs)
        self.files = []
        for file in files:
            path = Path(file)
            if path.is_file():
                self.files.append(file)

    def getFiles(self):
        returnFiles = []
        for file in self.files:
            path = Path(file)
            if path.is_file():
                returnFiles.append(file)
        return returnFiles

    def data(self, index, role=None):
        if index.isValid() and role == Qt.DisplayRole:
            # creez obiect tip Path din modulul pathlib ca sa pot face diverse operatii pe calea fisierului
            file = Path(self.files[index.row()])
            return file.name
        return None

    def rowCount(self, parent=None):
        return len(self.files)


class GradesTableModel(QAbstractTableModel):
    def __init__(self, data: list):
        super(GradesTableModel, self).__init__()
        self.columnLabels = ['Subject', 'Grade', 'Credits']
        self._data = data    # lista de dictionare

    def data(self, index, role=None):
        if index.isValid() and role is not None:
            if role == Qt.DisplayRole:
                # index elem in lista si cheia pt dict (numele coloanei)
                return self._data[index.row()][self.columnLabels[index.column()]]
            if role == Qt.TextAlignmentRole:
                if index.column() in [0, 1, 2]:
                    return Qt.AlignVCenter + Qt.AlignHCenter
        return None

    def rowCount(self, parent=None):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, parent=None):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.columnLabels[section]
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)


class TicketsTableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TicketsTableModel, self).__init__()
        self._data = data    # data frame ul citit din csv

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=None):
        if index.isValid() and role is not None:
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
            if role == Qt.TextAlignmentRole:
                return Qt.AlignVCenter + Qt.AlignHCenter
        return None

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[section]
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)
