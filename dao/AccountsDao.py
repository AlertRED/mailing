from Exception import UserError
from model.AccountsModel import AccountsModel
from model.ValidateModel import ValidateModel
from settings import Settings


class AccountsDao:

    def __init__(self, accounts_model: AccountsModel, validate_model: ValidateModel, settings: Settings):
        self.accounts_model = accounts_model
        self.validate_model = validate_model
        self.settings = settings

        self.is_single = None
        self.email = None
        self.password = None
        self.path_txt = None

    def test_account(self, email, password):
        if not self.validate_model.is_validate_email(email):
            raise UserError('Email is not validate')
        else:
            return self.accounts_model.is_account_connected(email, password)

    def save_settings(self, is_single, email, password, path_txt):
        if is_single:
            self.accounts_model.set_account(email, password)
        else:
            self.accounts_model.set_accounts_from_file(path_txt)
        self.settings.add_settings({'is_single': is_single, 'email': email, 'password': password, 'path_txt': path_txt})

    def load_settings(self):
        self.is_single = self.settings.get_settings('is_single')
        self.email = self.settings.get_settings('email')
        self.password = self.settings.get_settings('password')
        self.path_txt = self.settings.get_settings('path_txt')

        if self.is_single:
            self.accounts_model.set_account(self.email, self.password)
        else:
            self.accounts_model.set_accounts_from_file(self.path_txt)

    def get_settings(self):
        return self.is_single, self.email, self.password, self.path_txt
