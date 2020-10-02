import threading

from view.AccountsWindowView import AccountsWindowView


class AccountsController:

    def __init__(self, model):
        self.accounts_view = AccountsWindowView()
        self.model = model
        self.init()

    def init(self):
        self.accounts_view.select_button_single_signal.connect(self.select_button_single)
        self.accounts_view.select_button_multiple_signal.connect(self.select_button_multiple)
        self.accounts_view.change_login_signal.connect(self.change_login)
        self.accounts_view.change_password_signal.connect(self.change_password)
        self.accounts_view.change_path_accounts.connect(self.change_path_accounts)
        self.accounts_view.test_login_signal.connect(self.test_account)
        self.accounts_view.accept_signal.connect(self.accept)
        self.password = ""
        self.login = ""
        self.path_accounts = ""
        self.is_single = True

    def test_account(self):
        def foo(login, password):
            if self.model.test_connection(login, password):
                self.accounts_view.show_info('Account is connected')
            else:
                self.accounts_view.show_error('Account not is connected')
        x = threading.Thread(target=foo, args=(self.login, self.password,))
        x.start()

    def change_login(self, text):
        self.login = text
        self.change_test_button()
        self.enable_accept()

    def change_password(self, text):
        self.password = text
        self.change_test_button()
        self.enable_accept()

    def change_test_button(self):
        not_empty = self.is_single and self.login != '' and self.password != ''
        self.accounts_view.show_test(not_empty)

    def change_path_accounts(self, path):
        self.path_accounts = path
        self.enable_accept()

    def select_button_multiple(self):
        self.is_single = False
        self.accounts_view.show_single_part(False)
        self.accounts_view.show_multiple_part(True)
        self.enable_accept()

    def select_button_single(self):
        self.is_single = True
        self.accounts_view.show_single_part(True)
        self.accounts_view.show_multiple_part(False)
        self.change_test_button()
        self.enable_accept()

    def change_enable_part(self):
        if self.is_single:
            self.accounts_view.select_single_part()
        else:
            self.accounts_view.select_multiple_part()

    def enable_accept(self):
        if self.is_single:
            not_empty = self.login != '' and self.password != ''
        else:
            not_empty = self.path_accounts != ''
        self.accounts_view.enable_accept(not_empty)

    def accept(self):
        self.model.accept_accounts(self.login, self.password, self.is_single, self.path_accounts)
        self.accounts_view.close()

    def run(self):
        self.change_enable_part()
        self.change_test_button()
        self.enable_accept()
        self.accounts_view.show()

