import sys
from PyQt5 import QtWidgets

from Exception import UserError
from dao.AccountsDao import AccountsDao
from dao.DataDao import DataDao
from dao.MainDao import MainDao
from view.MainWindowView import MainWindowView
from view.AccountsWindowView import AccountsWindowView
from view.DataWindowView import DataWindowView
from model.Model import Model


class Controller():

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        self.model = Model()

        self.mainDao = MainDao(self.model, self)
        self.mainView = MainWindowView(self)

        self.dataDao = DataDao(self.model)
        self.dataView = DataWindowView(self)
        self.load_settings_data()

        self.accountsDao = AccountsDao(self.model, self)
        self.accountsView = AccountsWindowView(self)
        self.load_settings_accounts()

    def save_account_settings(self, is_single, email, password, path_txt):
        self.accountsDao.save_settings(is_single, email, password, path_txt)

    def test_account(self, email, password):
        try:
            is_connected = self.accountsDao.test_account(email, password)
            if is_connected:
                self.accountsView.showInfo('Account is connected')
            else:
                self.accountsView.showInfo('Account NOT is connected')
        except UserError as e:
            self.accountsView.showError(e)

    def set_email_column(self, text):
        self.model.set_email_column(text)

    def load_xlsx(self, path):
        self.dataDao.set_xlsx(path)
        sheets = self.dataDao.get_sheets()
        self.dataView.show_sheets(sheets)

    def select_email(self, text):
        self.dataDao.set_email_column(text)

    def select_sheet(self, text):
        data = self.dataDao.load_sheet(text)
        self.dataView.show_xlsx(data)

    def save_data_settings(self, path_xlsx, sheet, email_column, message):
        self.dataDao.save_settings(path_xlsx, sheet, email_column, message)

    def open_data_window(self):
        self.dataView.show()

    def open_accounts_window(self):
        self.accountsView.show()

    def load_settings_accounts(self):
        is_single, email, password, path_txt = self.accountsDao.load_settings()
        self.accountsView.load_settings(is_single, email, password, path_txt)

    def load_settings_data(self):
        path_xlsx, sheet, email_column, message = self.dataDao.load_settings()
        self.dataView.load_settings(path_xlsx, sheet, email_column, message)

    def start_app(self):
        self.mainView.show()
        self.app.exec_()
