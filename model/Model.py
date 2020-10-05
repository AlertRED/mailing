import os
import re
from time import sleep
import pandas as pd

from Exception import UserError
from support.mailing import SMTP, Mailing


class Model:

    def __init__(self):
        super().__init__()
        self.current_index = 0
        self.password = ""
        self.email = ""
        self.path_accounts = ""
        self.is_single = True

        self.path_xlsx = ""
        self.sheet_name = ""
        self.email_header = ""
        self.title = ""
        self.message = ""
        self.headers = list()
        self.fields = list()
        self.attachments = list()

        self.count_connections = 3

        self.is_play = False
        self.is_pause = False

        self.is_test = True
        self.accounts = list()

        self.filter_to = False
        self.filter_from = False
        self.filter_title = False
        self.filter_message = False

    def test_connection(self, login, password):
        smtp = SMTP()
        return smtp.login(login, password)

    def get_sheets(self, path):
        _, file_extension = os.path.splitext(path)
        if file_extension == '.xlsx':
            if os.path.isfile(path):
                file = pd.ExcelFile(path)
                return file.sheet_names
            else:
                raise UserError('File not exist')
        else:
            raise UserError('File is not xlsx')

    def get_xlsx(self, path, sheet):
        file = pd.ExcelFile(path)
        data_dict = file.parse(sheet, dtype=str).fillna('').to_dict("list")
        fields = list(zip(*data_dict.values()))
        headers = list(data_dict.keys())
        return headers, fields

    def find_accounts_from_file(self, path):
        accounts = []
        is_validate_email = lambda email: re.match(r'[^@]+@[^@]+\.[^@]+', email)
        is_validate_password = lambda password: password != ''
        with open(path, 'r', encoding='utf8') as file:
            while True:
                line = file.readline().strip().replace('\n', '')
                if line:
                    account = line.split(':')
                    if len(account) == 2 \
                            and is_validate_email(account[0]) \
                            and is_validate_password(account[1]):
                        accounts.append(tuple(account))
                else:
                    break
        self.accounts = accounts

    def load_accounts(self):
        if self.is_single:
            if self.email == '' or self.password == '':
                raise UserError('Email or password is empty')
            self.accounts = [(self.email, self.password)]
        else:
            if self.path_accounts == '':
                raise UserError('Path accounts is empty')
            self.find_accounts_from_file(self.path_accounts)

    def start_mailing(self):
        self.load_accounts()
        if self.path_xlsx == '':
            raise UserError('Data are not selected')
        if len(self.accounts) == 0:
            raise UserError('Accounts are not selected')
        self.is_play = True
        self.is_pause = False

        return self.mailing()

    def pause_mailing(self):
        self.is_play = True
        self.is_pause = True

    def stop_mailing(self):
        self.current_index = 0
        self.is_play = False
        self.is_pause = False

    def mailing(self):
        total_rows = len(self.fields)
        total_emails = len(self.accounts)
        email_index = self.headers.index(self.email_header)

        mail = Mailing(self.accounts)

        for index in range(self.current_index, total_rows):
            if self.is_pause or not self.is_play:
                break

            row = self.fields[index]
            args = {header: row[i] for i, header in enumerate(self.headers)}

            _to = row[email_index]
            _body = self.message.format(**args)
            _title = self.title.format(**args)

            if not self.is_test:
                index_account, _from = mail.send_mail(_to, _title, _body, self.attachments)
            else:
                index_account, _from = 1, self.accounts[0][0]

            self.current_index = index

            msg = dict()
            if self.filter_to:
                msg['from'] = _from
            if self.filter_from:
                msg['to'] = _to
            if self.filter_title:
                msg['title'] = _title
            if self.filter_message:
                msg['body'] = _body

            yield {'current_sent': self.current_index + 1, 'total_sent': total_rows, 'current_email': _from,
                   'index_account': index_account, 'total_emails': total_emails, 'message': msg}
            sleep(1)

    def accept_accounts(self, email, password, is_single, path_accounts):
        self.email = email
        self.password = password
        self.is_single = is_single
        self.path_accounts = path_accounts

    def accept_data(self, title, message, path_xlsx, sheet_name, email_header, headers, fields, attachments):
        self.title = title
        self.message = message
        self.path_xlsx = path_xlsx
        self.sheet_name = sheet_name
        self.email_header = email_header
        self.headers = headers
        self.fields = fields
        self.attachments = attachments

