import sys
import threading

from PyQt5 import QtWidgets

from Exception import UserError
from controller.AccountsController import AccountsController
from controller.DataController import DataController

from view.MainWindowView import MainWindowView

from model.Model import Model
from time import gmtime


class Controller:

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
        self.mainView.start_without_test_message.connect(self.absolute_start)

        self.mainView.check_filter_to_signal.connect(self.filter_to)
        self.mainView.check_filter_from_signal.connect(self.filter_from)
        self.mainView.check_filter_title_signal.connect(self.filter_title)
        self.mainView.check_filter_message_signal.connect(self.filter_message)


    def start(self):
        if self.model.is_test:
                self.absolute_start(True)
        else:
            self.mainView.show_no_test_message()

    def pause(self):
        if self.model.is_play:
            self.mainView.pause_mailing()
            self.print_message('Pause')
            self.model.pause_mailing()

    def stop(self):
        if self.model.is_play:
            self.mainView.stop_mailing()
            self.print_message('Stop')
            self.model.stop_mailing()

    def absolute_start(self, is_start):
        if is_start:
            try:
                mailing = self.model.start_mailing()
            except UserError as e:
                self.mainView.show_error(str(e))
            else:
                self.mainView.start_mailing()
                self.print_message('Start')
                self.mailing(mailing)

    def mailing(self, mailing):
        def foo(print_log, show_progress, show_emails_stat, messages):
            message_keys = ('from', 'to', 'title', 'body')
            while True:
                try:
                    feed_back = next(messages)
                except UserError as e:
                    self.mainView.show_error(str(e))
                except StopIteration:
                    break
                else:
                    message = feed_back.get('message')
                    if message:
                        text = '\n'.join(message.get(key) for key in message_keys if message.get(key))
                        print_log(text)

                    email_connected = feed_back.get('email_connected')
                    if email_connected:
                        print_log(f"Connected to {email_connected}")

                    email_not_connected = feed_back.get('email_not_connected')
                    if email_not_connected:
                        print_log(f"Connected wrong to {email_not_connected}")

                    current_sent, total_sent = feed_back.get('current_sent'), feed_back.get('total_sent')
                    if current_sent and total_sent:
                        show_progress(current_sent, total_sent)

                    current_email, index_account, total_emails = feed_back.get('current_email'), feed_back.get('index_account'), feed_back.get('total_emails')
                    if current_email and index_account and total_emails:
                        show_emails_stat(current_email, index_account, total_emails)

        x = threading.Thread(target=foo, args=(
        self.print_message, self.show_progress, self.show_emails_stat, mailing,))
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

    def open_data_window(self):
        self.data_controller.run()

    def open_accounts_window(self):
        self.accounts_controller.run()

    def filter_to(self, is_checked):
        self.model.filter_to = is_checked

    def filter_from(self, is_checked):
        self.model.filter_from = is_checked

    def filter_title(self, is_checked):
        self.model.filter_title = is_checked

    def filter_message(self, is_checked):
        self.model.filter_message = is_checked

    def start_app(self):
        self.mainView.stop_mailing()
        self.mainView.test_checked(True)
        self.mainView.show()
        self.app.exec_()
