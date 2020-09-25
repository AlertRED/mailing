import re


class Model:

    def __init__(self):
        self.accounts = list()
        self.message = str()
        self.emails = list()
        self.fields = dict()

    def is_validate_email(self, email):
        return re.match(r'[^@]+@[^@]+\.[^@]+', email)

    def is_validate_password(self, password):
        return password != ''

    def is_account_connected(self, email, password):
        return self.is_validate_email(email)


    def findAccountsFromFile(self, path):
        self.accounts.clear()
        with open(path, 'r', encoding='utf8') as file:
            while True:
                line = file.readline().strip().replace('\n', '')
                if line:
                    account = line.split(':')
                    if len(account) == 2 and self.is_validate_password(account[0]) and self.is_validate_email(account[0]):
                        self.accounts.append(tuple(account))
                else:
                    break

    def getCountAccounts(self):
        return len(self.accounts)
