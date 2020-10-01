from view.AccountsWindowView import AccountsWindowView


class AccountsController:

    def __init__(self, model):
        self.accountsView = AccountsWindowView()
        self.model = model
        self.init()

    def init(self):
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

    def run(self):
        self.change_enable_part()
        self.change_test_button()
        self.enable_accept()
        self.accountsView.show()

