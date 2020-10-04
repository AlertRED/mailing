import sys
import threading

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject

from Exception import UserError
from controller.AccountsController import AccountsController
from controller.DataController import DataController

from view.MainWindowView import MainWindowView

from model.Model import Model
from time import gmtime


class Controller(QObject):

    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication(sys.argv)
        self.model = Model()
        self.mainView = MainWindowView()
        self.accounts_controller = AccountsController(self.model)
        self.data_controller = DataController(self.model)
        self.init()

    def init(self):
        self.mainView.open_data_signal.connect(self.open_data_window)
        self.mainView.open_accounts_signal.connect(self.open_accounts_window)
        self.mainView.test_only_signal.connect(self.test_only)
        self.mainView.start_signal.connect(self.start)
        self.mainView.pause_signal.connect(self.pause)
        self.mainView.stop_signal.connect(self.stop)

    def start(self):
        try:
            self.model.validate_data_for_mailing()
        except UserError as e:
            self.mainView.show_error(str(e))
        else:
            self.mainView.test_enable(False)
            self.mainView.state_player(False, True, True)
            self.model.is_play = True
            self.model.is_pause = False
            self.print_message('Start')
            self.model.load_accounts()
            self.mailing()

    def mailing(self):
        def foo(print_log, show_progress, show_emails_stat, messages):
            for feed_back in messages:
                message = feed_back.get('message')
                if message:
                    text = ''
                    text += message.get('from', '') + '\n'
                    text += message.get('to', '') + '\n'
                    text += message.get('title', '') + '\n'
                    text += message.get('body', '')
                    print_log(text)

                email_connected = feed_back.get('email_connected')
                if email_connected:
                    print_log(f"Connected to {email_connected}")

                email_not_connected = feed_back.get('email_not_connected')
                if email_not_connected:
                    print_log(f"Connected wrong to {email_not_connected}")

                current_send, total_send = feed_back.get('current_send'), feed_back.get('total_send')
                if current_send and total_send:
                    show_progress(current_send, total_send)

                current_email, index_email, total_emails = feed_back.get('current_email'), feed_back.get('index_email'), feed_back.get('total_emails')
                if current_email and index_email and total_emails:
                    show_emails_stat(current_email, index_email, total_emails)

        x = threading.Thread(target=foo, args=(
        self.print_message, self.show_progress, self.show_emails_stat, self.model.mailing(),))
        x.start()

    def print_message(self, text):
        time = gmtime()
        self.mainView.print_log_signal.emit(text, time)

    def show_progress(self, count, total):
        self.mainView.print_progress_signal.emit(count, total)

    def show_emails_stat(self, email, count, total):
        self.mainView.print_email_stat_signal.emit(email, count, total)

    def test_only(self, is_test):
        self.model.is_test = is_test

    def pause(self):
        if self.model.is_play:
            self.model.is_pause = True
            self.print_message('Pause')
            self.mainView.state_player(True, False, True)

    def stop(self):
        if self.model.is_play:
            self.mainView.test_enable(True)
            self.model.is_play = False
            self.model.is_pause = False
            self.print_message('Stop')
            self.model.current_index = 0
            self.mainView.state_player(True, False, False)

    def open_data_window(self):
        self.data_controller.run()

    def open_accounts_window(self):
        self.accounts_controller.run()

    def start_app(self):
        self.mainView.state_player(True, False, False)
        self.mainView.test_checked(True)
        self.mainView.show()
        self.app.exec_()
