from PyQt5.QtWidgets import QDialog, QFileDialog, QAbstractItemView

from ui.design.robotAttachmentsDialog import Ui_AttachDialog
from ui.util.models import FilesListModel


class AttachDialogLogic(QDialog, Ui_AttachDialog):

    def __init__(self, parent=None, files=None):
        super(AttachDialogLogic, self).__init__(parent)
        if files is None:
            files = []
        self.parent = parent
        self.setupUi(parent)
        self.filesModel = FilesListModel(files=files)
        self.filesListView.setModel(self.filesModel)  # ii atribui view-ului modelul creat mai sus
        self.filesListView.setSelectionMode(QAbstractItemView.ExtendedSelection)  # selectie extinsa/multipla

        self.addButton.clicked.connect(self.addFiles)
        self.deleteButton.clicked.connect(self.deleteFiles)
        self.okButton.clicked.connect(self.ok)

    def getFiles(self):
        return self.filesModel.getFiles()

    def addFiles(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Attach files",
                                                    "", "All Files (*);;Text Files (*.txt);;PDFs (*.pdf);;" + \
                                                    "Rar files (*rar);;Zip files (*zip);;Docs (*doc);;Docxs (*docx)" + \
                                                    ";;CSVs (*csv);;Excels (*xlsx)")
        if files:
            existentFiles = self.filesModel.getFiles()
            for file in files:
                if file not in existentFiles:
                    self.filesModel.files.append(file)
            self.filesModel.layoutChanged.emit()  # ii semnalez view-ului ca s-a schimbat modelul

    def deleteFiles(self):
        indexes = self.filesListView.selectedIndexes()
        for index in indexes:
            del self.filesModel.files[index.row()]
        self.filesListView.clearSelection()
        self.filesModel.layoutChanged.emit()

    def exec_(self) -> int:
        return self.parent.exec_()

    def ok(self):
        self.parent.accept()
