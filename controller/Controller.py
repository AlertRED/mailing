import sys
from PyQt5 import QtWidgets

from dao.AccountsDao import AccountsDao
from dao.DataDao import DataDao
from dao.MainDao import MainDao
from view.MainWindowView import MainWindowView
from view.AccountsWindowView import AccountsWindowView
from view.DataWindowView import DataWindowView
from view.qt import AccountsWindow, MainWindow, DataWindow
from model.Model import Model


class Controller():

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        self.model = Model()

        self.mainDao = MainDao(self.model, self)
        self.mainWindow = MainWindow.Ui_MainWindow()
        self.mainWindowModel = MainWindowView(self.mainDao)

        self.dataDao = DataDao(self.model, self)
        self.dataWindow = DataWindow.Ui_MainWindow()
        self.dataWindowModel = DataWindowView(self.dataDao)

        self.accountsDao = AccountsDao(self.model, self)
        self.accountsWindow = AccountsWindow.Ui_MainWindow()
        self.accountsWindowModel = AccountsWindowView(self.accountsDao)


    def start_app(self):
        self.mainWindowModel.show()
        self.app.exec_()
