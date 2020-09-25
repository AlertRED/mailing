from PyQt5 import QtWidgets
from view.qt import MainWindow


class MainWindowView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super().__init__()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.controller = controller
        self.ui.actionData.triggered.connect(self.onClickActionData)
        self.ui.actionAccounts.triggered.connect(self.onClickActionAccounts)

    def onClickActionData(self):
        self.controller.openDataWindow()

    def onClickActionAccounts(self):
        self.controller.openAccountsWindow()
