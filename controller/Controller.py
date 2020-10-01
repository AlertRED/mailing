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
    print_progress = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication(sys.argv)

        self.settings = Settings()
        self.settings.load_settings()

        self.validate_model = ValidateModel()
        self.accounts_model = AccountsModel(self.validate_model)
        self.xlsx_model = XlsxModel()
        self.mailing_model = MailingModel(self.accounts_model, self.settings)

        self.mainView = MainWindowView(self)

        self.mainDao = MainDao(self.mailing_model, self.xlsx_model, self, self.settings)
        self.dataDao = DataDao(self.validate_model, self.settings, self.xlsx_model)
        self.accountsDao = AccountsDao(self.accounts_model, self.validate_model, self.settings)

        self.dataDao.load_settings()
        self.accountsDao.load_settings()

        self.print_log.connect(self.mainView.print_log)
        self.print_progress.connect(self.mainView.print_progress)

        self.mainView.show_filters_checkboxes(['From', 'To', 'Title', 'Message'],
                                              [self.change_state_from, self.change_state_to, self.change_state_title,
                                 self.change_state_message])
        self.is_from = False
        self.is_to = False
        self.is_title = False
        self.is_message = False

    def change_state_from(self, is_from):
        self.is_from = is_from

    def change_state_to(self, is_to):
        self.is_to = is_to

    def change_state_title(self, is_title):
        self.is_title = is_title

    def change_state_message(self, is_message):
        self.is_message = is_message

    def save_account_settings(self, is_single, email, password, path_txt):
        self.accountsDao.save_settings(is_single, email, password, path_txt)

    def test_account(self, email, password):
        try:
            is_connected = self.accountsDao.test_account(email, password)
            if is_connected:
                self.accountsView.show_info('Account is connected')
            else:
                self.accountsView.show_info('Account NOT is connected')
        except UserError as e:
            self.accountsView.show_error(e)

    def load_sheets(self, path):
        self.dataDao.load_xlsx(path)
        sheets = self.dataDao.get_sheets()
        self.dataView.show_sheets(sheets)

    def select_sheet(self, text):
        data = self.dataDao.load_sheet(text)
        self.dataView.show_xlsx(data[0], data[1])

    def save_data_settings(self, path_xlsx, sheet, email_column, message, title):
        self.dataDao.save_settings(path_xlsx, sheet, email_column, message, title)

    def open_data_window(self):
        self.dataView = DataWindowView(self)
        self.load_settings_data()
        self.dataView.show()

    def open_accounts_window(self):
        self.accountsView = AccountsWindowView(self)
        self.load_settings_accounts()
        self.accountsView.show()

    def load_settings_accounts(self):
        is_single, email, password, path_txt = self.accountsDao.get_settings()
        self.accountsView.load_settings(is_single, email, password, path_txt)

    def load_settings_data(self):
        path_xlsx, sheet, email_column, message, title = self.dataDao.get_settings()
        self.dataView.load_settings(path_xlsx, sheet, email_column, message, title)

    def start_mailing(self):

        def foo(print_log, print_progress):
            for info in self.mainDao.mailing():
                message = info['message']
                text = ''
                if self.is_to:
                    text += f'To: {message["to"]}\n'
                if self.is_from:
                    text += f'From: {message["from"]}\n'
                if self.is_title:
                    text += f'Title: {message["title"]}\n'
                if self.is_message:
                    text += f'Message: {message["body"]}\n'
                print_log.emit(text, True)
                print_progress.emit(info['count'], info['total'])

        x = threading.Thread(target=foo, args=(self.print_log, self.print_progress,))
        x.start()


    def stop_mailing(self):
        self.mainDao.stop_mailing()
        self.print_progress.emit(0, 0)

    def pause_mailing(self):
        self.mainDao.pause_mailing()

    def start_app(self):
        self.mainView.show()
        self.app.exec_()
