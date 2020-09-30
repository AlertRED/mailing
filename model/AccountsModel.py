from model.ValidateModel import ValidateModel


class AccountsModel():
    def __init__(self, validate: ValidateModel):
        self.accounts = list()
        self.validate = validate

    def findAccountsFromFile(self, path):
        accounts = []
        with open(path, 'r', encoding='utf8') as file:
            while True:
                line = file.readline().strip().replace('\n', '')
                if line:
                    account = line.split(':')
                    if len(account) == 2 and self.validate.is_validate_password(
                            account[0]) and self.validate.is_validate_email(
                        account[0]):
                        accounts.append(tuple(account))
                else:
                    break
        return accounts

    def set_account(self, email, password):
        self.accounts = [(email, password)]

    def set_accounts_from_file(self, path):
        self.accounts = self.findAccountsFromFile(path)

    def get_account(self):
        for account in self.accounts:
            yield account

    def getCountAccounts(self):
        return len(self.accounts)

    def is_account_connected(self, email, password):
        return self.validate.is_validate_email(email)
