from PyQt5 import QtWidgets
from view.qt import MainWindow

class MainWindowView(QtWidgets.QMainWindow):

    def __init__(self, dao):
        super().__init__()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.dao = dao
        self.ui.actionData.triggered.connect(self.onClickActionData)
        self.ui.actionAccounts.triggered.connect(self.onClickActionAccounts)

    def onClickActionData(self):
        self.dao.openDataWindow()

    def onClickActionAccounts(self):
        self.dao.openAccountsWindow()
