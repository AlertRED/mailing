
class AccountsDao:

    def __init__(self, model, controller):
        self.model = model
        self.controller = controller

    def onClickTestAccount(self, email, password):
        if not self.model.is_validate_email(email):
            self.controller.accountsWindowModel.showEmailNotValidate()
        else:
            is_connected = self.model.is_account_connected(email, password)
            self.controller.accountsWindowModel.showAccountIsConnected(is_connected)
