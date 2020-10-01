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
from model.Model import Model


class Controller(QObject):
    print_log = pyqtSignal(str, bool)
    print_progress = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication(sys.argv)
        self.model = Model()
        # self.settings = Settings()
        # self.settings.load_settings()

        # self.validate_model = ValidateModel()
        # self.accounts_model = AccountsModel(self.validate_model)
        # self.xlsx_model = XlsxModel()
        # self.mailing_model = MailingModel(self.accounts_model, self.settings)
        self.mainView = MainWindowView()
        self.dataView = DataWindowView()
        self.accountsView = AccountsWindowView()
        #
        # self.mainDao = MainDao(self.mailing_model, self.xlsx_model, self, self.settings)
        # self.dataDao = DataDao(self.validate_model, self.settings, self.xlsx_model)
        # self.accountsDao = AccountsDao(self.accounts_model, self.validate_model, self.settings)

        # self.dataDao.load_settings()
        # self.accountsDao.load_settings()

        # self.print_log.connect(self.mainView.print_log)
        # self.print_progress.connect(self.mainView.print_progress)

        # self.mainView.show_filters_checkboxes(['From', 'To', 'Title', 'Message'],
        #                                       [self.change_state_from, self.change_state_to, self.change_state_title,
        #                          self.change_state_message])
        # self.is_from = False
        # self.is_to = False
        # self.is_title = False
        # self.is_message = False
        self.init()

    def init(self):
        self.mainView.open_data_signal.connect(self.open_data_window)
        self.mainView.open_accounts_signal.connect(self.open_accounts_window)
        self.accountsView.select_button_single_signal.connect(self.select_button_single)
        self.accountsView.select_button_multiple_signal.connect(self.select_button_multiple)
        self.accountsView.change_login_signal.connect(self.change_login)
        self.accountsView.change_password_signal.connect(self.change_password)
        self.accountsView.change_path_accounts.connect(self.change_path_accounts)

    def change_login(self, text):
        self.model.login = text
        self.change_test_button()
        self.enable_accept()

    def change_password(self, text):
        self.model.password = text
        self.change_test_button()
        self.enable_accept()

    def change_test_button(self):
        not_empty = self.model.is_single and self.model.login != '' and self.model.password != ''
        self.accountsView.show_test(not_empty)

    def change_path_accounts(self, path):
        self.model.path_accounts = path
        self.enable_accept()

    def select_button_multiple(self):
        self.model.is_single = False
        self.accountsView.show_single_part(False)
        self.accountsView.show_multiple_part(True)
        self.enable_accept()

    def select_button_single(self):
        self.model.is_single = True
        self.accountsView.show_single_part(True)
        self.accountsView.show_multiple_part(False)
        self.change_test_button()
        self.enable_accept()

    def change_enable_part(self):
        if self.model.is_single:
            self.accountsView.select_single_part()
        else:
            self.accountsView.select_multiple_part()





    def enable_accept(self):
        if self.model.is_single:
            not_empty = self.model.login != '' and self.model.password != ''
        else:
            not_empty = self.model.path_accounts != ''
        self.accountsView.enable_accept(not_empty)


    # def change_state_from(self, is_from):
    #     self.is_from = is_from
    #
    # def change_state_to(self, is_to):
    #     self.is_to = is_to
    #
    # def change_state_title(self, is_title):
    #     self.is_title = is_title
    #
    # def change_state_message(self, is_message):
    #     self.is_message = is_message
    #
    # def save_account_settings(self, is_single, email, password, path_txt):
    #     self.accountsDao.save_settings(is_single, email, password, path_txt)
    #
    # def test_account(self, email, password):
    #     try:
    #         is_connected = self.accountsDao.test_account(email, password)
    #         if is_connected:
    #             self.accountsView.show_info('Account is connected')
    #         else:
    #             self.accountsView.show_info('Account NOT is connected')
    #     except UserError as e:
    #         self.accountsView.show_error(e)
    #
    # def load_sheets(self, path):
    #     self.dataDao.load_xlsx(path)
    #     sheets = self.dataDao.get_sheets()
    #     self.dataView.show_sheets(sheets)
    #
    # def select_sheet(self, text):
    #     data = self.dataDao.load_sheet(text)
    #     self.dataView.show_xlsx(data[0], data[1])
    #
    # # def save_data_settings(self, path_xlsx, sheet, email_column, message, title):
    # #     self.dataDao.save_settings(path_xlsx, sheet, email_column, message, title)
    def open_data_window(self):
        self.dataView.show()

    def open_accounts_window(self):
        self.change_enable_part()
        self.change_test_button()
        self.enable_accept()
        self.accountsView.show()

    # def load_settings_accounts(self):
    #     is_single, email, password, path_txt = self.accountsDao.get_settings()
    #     self.accountsView.load_settings(is_single, email, password, path_txt)
    #
    # def load_settings_data(self):
    #     path_xlsx, sheet, email_column, message, title = self.dataDao.get_settings()
    #     self.dataView.load_settings(path_xlsx, sheet, email_column, message, title)
    #
    # def start_mailing(self):
    #
    #     def foo(print_log, print_progress):
    #         for info in self.mainDao.mailing():
    #             message = info['message']
    #             text = ''
    #             if self.is_to:
    #                 text += f'To: {message["to"]}\n'
    #             if self.is_from:
    #                 text += f'From: {message["from"]}\n'
    #             if self.is_title:
    #                 text += f'Title: {message["title"]}\n'
    #             if self.is_message:
    #                 text += f'Message: {message["body"]}\n'
    #             print_log.emit(text, True)
    #             print_progress.emit(info['count'], info['total'])
    #
    #     x = threading.Thread(target=foo, args=(self.print_log, self.print_progress,))
    #     x.start()
    #
    #
    # def stop_mailing(self):
    #     self.mainDao.stop_mailing()
    #     self.print_progress.emit(0, 0)
    #
    # def pause_mailing(self):
    #     self.mainDao.pause_mailing()

    def start_app(self):
        self.mainView.show()
        self.app.exec_()
