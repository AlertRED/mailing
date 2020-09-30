import smtplib
from email.header import Header
from email.mime.text import MIMEText
from time import sleep

from model.AccountsModel import AccountsModel
from settings import Settings


class MailingModel:

    def __init__(self, accounts: AccountsModel, settings: Settings):
        self.is_pause = False
        self.is_start = False
        self.settings = settings
        self.accounts = accounts
        self.smtp = SMTP()

    def pause_mailing(self):
        self.is_pause = True

    def stop_mailing(self):
        self.is_start = False
        self.is_pause = False
        self.settings.add_settings({'email_index': 0})

    def start_mailing(self, headers, fields, message_body_format, message_title_format, email_column, is_test):
        if not self.is_start or self.is_pause:
            self.is_start = True
            self.is_pause = False

            start_index = self.settings.get_settings('email_index', 0)
            return self.mailing(start_index, fields, headers, message_body_format, message_title_format, email_column,
                                is_test)

    def mailing(self, start_index: int, fields: list, headers: list, message_body_format: str, message_title_format,
                email_column,
                is_test):
        email_column_index = headers.index(email_column)
        accounts = self.accounts.get_account()
        own_email, own_password = next(accounts)
        if not is_test:
            self.smtp.login(own_email, own_password)

        total_count = len(fields)

        for index, row in enumerate(fields[start_index:]):
            if not self.is_start or self.is_pause:
                break

            args = {header: row[i] for i, header in enumerate(headers)}

            _to = row[email_column_index]
            _message = message_body_format.format(**args)
            _title = message_title_format.format(**args)

            if not is_test:
                self.smtp.send_message(_to, _title, _message)
            yield {'count': start_index + index, 'total': total_count,
                   'message': {'body': _message, 'title': _title, 'from': own_email, 'to': _to}}

            self.settings.add_settings({'email_index': start_index + index + 1})
            sleep(1)


class SMTP:
    def __init__(self):
        self.email = None
        self.password = None
        self.smtpObj = None

    def get_message(self, to, from1, text, title):
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['Subject'] = Header(title, 'utf-8')
        msg['From'] = from1
        msg['To'] = to
        return msg

    def connect_smtp(self, smtp_adress, port=587):
        self.smtpObj = smtplib.SMTP(smtp_adress, port, timeout=10)
        self.smtpObj.starttls()

    def login(self, email, password):
        smtp_adress = 'smtp.' + self.email.split('@')[1]
        self.connect_smtp(smtp_adress)
        self.email = email
        self.password = password

    def send_message(self, _to, _title, _message):
        message = self.get_message(_to, self.email, _message, _title)
        # self.smtpObj.sendmail(self.email, _to, message.as_string())
