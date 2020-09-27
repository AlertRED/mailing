from Exception import UserError

class AccountsDao:

    def __init__(self, model, controller):
        self.model = model

    def test_account(self, email, password):
        if not self.model.is_validate_email(email):
            raise UserError('Email is not validate')
        else:
            return self.model.is_account_connected(email, password)

    def save_settings(self, is_single, email, password, path_txt):
        self.model.save_settings("Accounts",
                                {'is_single': is_single, 'email': email, 'password': password, 'path_txt': path_txt})

    def load_settings(self):
        settings = self.model.get_settings("Accounts")
        return settings.get('is_single'), settings.get('email'), settings.get('password'), settings.get('path_txt')
