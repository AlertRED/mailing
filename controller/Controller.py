import sys
from PyQt5 import QtWidgets
from view.MainWindowView import MainWindowView
from view.AccountsWindowView import AccountsWindowView
from view.DataWindowView import DataWindowView
from view.qt import AccountsWindow, MainWindow, DataWindow
from model.Model import Model

class Controller():

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication

        self.mainWindow = MainWindow.Ui_MainWindow()
        self.mainWindowModel = MainWindowView(self)  # Создаём объект класса ExampleApp

        self.dataWindow = DataWindow.Ui_MainWindow()
        self.dataWindowModel = DataWindowView(self)

        self.accountsWindow = AccountsWindow.Ui_MainWindow()
        self.accountsWindowModel = AccountsWindowView(self)

        self.model = Model()

    def start_app(self):
        self.mainWindowModel.show()
        self.accountsWindowModel.show()
        self.app.exec_()

    def openDataWindow(self):
        self.dataWindowModel.show()

    def openAccountsWindow(self):
        self.accountsWindowModel.show()

    def onClickTestAccount(self, email, password):
        if not self.model.is_validate_email(email):
            self.accountsWindowModel.showEmailNotValidate()
        else:
            is_connected = self.model.is_account_connected(email, password)
            self.accountsWindowModel.showAccountIsConnected(is_connected)


