class AccountsDao:

    def __init__(self, model, controller):
        self.model = model
        self.controller = controller

    def test_account(self, email, password):
        if not self.model.is_validate_email(email):
            self.controller.accountsView.showEmailNotValidate()
        else:
            is_connected = self.model.is_account_connected(email, password)
            self.controller.accountsView.showAccountIsConnected(is_connected)

    def save_settings(self, is_single, email, password, path_txt):
        self.model.save_settings("Accounts",
                                {'is_single': is_single, 'email': email, 'password': password, 'path_txt': path_txt})

    def load_settings(self):
        settings = self.model.get_settings("Accounts")
        self.controller.accountsView.load_settings(settings.get('is_single'), settings.get('email'),
                                                   settings.get('password'), settings.get('path_txt'))
