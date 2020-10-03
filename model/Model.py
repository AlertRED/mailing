import re
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from time import sleep

import pandas as pd

from Exception import UserError


class Model:

    def __init__(self):
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

        self.count_connections = 3

        self.is_play = False
        self.is_pause = False

        self.is_test = True
        self.accounts = list()

    def test_connection(self, login, password):
        smtp = SMTP()
        return smtp.login(login, password)

    def get_sheets(self, path):
        file = pd.ExcelFile(path)
        return file.sheet_names

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
            self.accounts = [(self.email, self.password)]
        else:
            self.find_accounts_from_file(self.path_accounts)

    def mailing(self):
        self.is_play = True
        total_rows = len(self.fields)
        total_emails = len(self.accounts)
        email_index = self.headers.index(self.email_header)

        smtp = SMTP()
        accounts = (account for account in self.accounts)

        email = None
        if self.is_test:
            email = next(accounts)[0]

        for index in range(self.current_index, total_rows):
            if self.is_pause or not self.is_play:
                break

            row = self.fields[index]
            args = {header: row[i] for i, header in enumerate(self.headers)}

            _to = row[email_index]
            _body = self.message.format(**args)
            _title = self.title.format(**args)

            if not self.is_test:
                if not smtp.is_connected():
                    for email, password in accounts:
                        if smtp.login(email, password):
                            yield {'email_connected': email}
                            break
                        yield {'email_not_connected': email}
                _from = email
                smtp.send_message(_to, _title, _body)
            else:
                _from = email


            self.current_index = index

            msg = dict()
            msg['from'] = _from
            msg['to'] = _to
            msg['title'] = _title
            msg['body'] = _body

            yield {'current_send': self.current_index + 1, 'total_send': total_rows, 'current_email': email, 'index_email': 1,
                   'total_emails': total_emails, 'message': msg}
            sleep(1)

    def accept_accounts(self, login, password, is_single, path_accounts):
        self.email = login
        self.password = password
        self.is_single = is_single
        self.path_accounts = path_accounts

    def accept_data(self, title, message, path_xlsx, sheet_name, email_header, headers, fields):
        self.title = title
        self.message = message
        self.path_xlsx = path_xlsx
        self.sheet_name = sheet_name
        self.email_header = email_header
        self.headers = headers
        self.fields = fields


class SMTP:
    def __init__(self):
        self.email = None
        self.password = None
        self.smtpObj = smtplib.SMTP()

    def is_connected(self)->bool:
        try:
            self.smtpObj.helo('')
            return True
        except smtplib.SMTPServerDisconnected:
            return False

    def get_message(self, to, from1, text, title):
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['Subject'] = Header(title, 'utf-8')
        msg['From'] = from1
        msg['To'] = to
        return msg

    def connect_smtp(self, port=587):
        smtp_adress = 'smtp.' + self.email.split('@')[1]
        self.smtpObj = smtplib.SMTP(smtp_adress, port, timeout=10)
        code = self.smtpObj.starttls()[0]
        return code == 220

    def is_validate_email(self, email):
        return re.match(r'[^@]+@[^@]+\.[^@]+', email)

    def login(self, email, password):
        if not self.is_validate_email(email):
            raise UserError('Email is not validate')
        self.email = email
        self.password = password
        if not self.connect_smtp():
            raise UserError('Error server connection')
        try:
            code = self.smtpObj.login(self.email, self.password)[0]
        except:
            raise UserError('Error login')
        return code == 235

    def send_message(self, _to, _title, _body):
        message = self.get_message(_to, self.email, _body, _title)
        # self.smtpObj.sendmail(self.email, _to, message.as_string())
