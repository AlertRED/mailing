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
        self.mainView = MainWindowView(self)

        self.dataDao = DataDao(self.model, self)
        self.dataView = DataWindowView(self)

        self.accountsDao = AccountsDao(self.model, self)
        self.accountsView = AccountsWindowView(self)

    def save_account_settings(self, is_single, email, password, path_txt):
        self.accountsDao.save_settings(is_single, email, password, path_txt)

    def test_account(self, email, password):
        self.accountsDao.test_account(email, password)

    def set_xlsx(self, path):
        self.dataDao.set_xlsx(path)

    def load_data_from_sheet(self, text):
        self.dataDao.load_data_from_sheet(text)

    def save_data_settings(self, path_xlsx, message):
        self.dataDao.save_settings(path_xlsx, message)

    def show_xlsx_on_data_window(self, data):
        self.dataView.show_xlsx(data)

    def open_data_window(self):
        self.dataView.show()

    def open_accounts_window(self):
        self.accountsView.show()

    def start_app(self):
        self.mainView.show()
        self.app.exec_()
