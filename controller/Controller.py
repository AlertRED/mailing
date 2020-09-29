import sys
import threading

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject

from Exception import UserError
from dao.AccountsDao import AccountsDao
from dao.DataDao import DataDao
from dao.MainDao import MainDao
from view.MainWindowView import MainWindowView
from view.AccountsWindowView import AccountsWindowView
from view.DataWindowView import DataWindowView
from model.ValidateModel import ValidateModel
from model.AccountsModel import AccountsModel
from model.XlsxModel import XlsxModel
from model.MailingModel import MailingModel
from settings import Settings


class Controller(QObject):
    print_log = pyqtSignal(str, bool)

    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication(sys.argv)

        self.settings = Settings()
        self.settings.load_settings()

        self.validate_model = ValidateModel()
        self.accounts_model = AccountsModel(self.validate_model)
        self.xlsx_model = XlsxModel()
        self.mailing_model = MailingModel(self.settings)

        self.mainDao = MainDao(self.mailing_model, self.xlsx_model, self, self.settings)
        self.mainView = MainWindowView(self)

        self.dataDao = DataDao(self.validate_model, self.settings, self.xlsx_model)
        self.dataView = DataWindowView(self)
        self.load_settings_data()

        self.accountsDao = AccountsDao(self.accounts_model, self.validate_model, self.settings)
        self.accountsView = AccountsWindowView(self)
        self.load_settings_accounts()

        self.print_log.connect(self.mainView.printLog)

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

    def load_xlsx(self, path):
        self.dataDao.load_xlsx(path)
        sheets = self.dataDao.get_sheets()
        self.dataView.show_sheets(sheets)

    def select_sheet(self, text):
        data = self.dataDao.load_sheet(text)
        self.dataView.show_xlsx(data[0], data[1])

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

    def start_mailing(self):

        def foo(print_log):
            for message in self.mainDao.mailing():
                print_log.emit(message, True)

        x = threading.Thread(target=foo, args=(self.print_log,))
        x.start()

    def stop_mailing(self):
        self.mainDao.stop_mailing()

    def pause_mailing(self):
        self.mainDao.pause_mailing()

    def start_app(self):
        self.mainView.show()
        self.app.exec_()
