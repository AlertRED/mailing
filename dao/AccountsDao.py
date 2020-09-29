from Exception import UserError
from model.AccountsModel import AccountsModel
from model.ValidateModel import ValidateModel
from settings import Settings


class AccountsDao:

    def __init__(self, accounts_model: AccountsModel, validate_model: ValidateModel, settings: Settings):
        self.accounts_model = accounts_model
        self.validate_model = validate_model
        self.settings = settings

    def test_account(self, email, password):
        if not self.validate_model.is_validate_email(email):
            raise UserError('Email is not validate')
        else:
            return self.accounts_model.is_account_connected(email, password)

    def save_settings(self, is_single, email, password, path_txt):
        self.settings.add_settings({'is_single': is_single, 'email': email, 'password': password, 'path_txt': path_txt})

    def load_settings(self):
        return self.settings.get_settings('is_single'), self.settings.get_settings('email'), self.settings.get_settings('password'), self.settings.get_settings('path_txt')
