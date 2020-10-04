import re
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from Exception import UserError


class Mailing:
    def __init__(self, accounts: list):
        self.accounts = accounts
        self.index_account = 0
        self.attempt_login = 3
        self.smtp = SMTP()

    def connect_smtp(self):
        is_connected = False
        for email, password in self.accounts[self.index_account:]:
            for _ in range(self.attempt_login):
                try:
                    self.smtp.login(email, password)
                    is_connected = True
                except UserError:
                    pass
            if is_connected:
                return email
            self.index_account += 1

    def send_mail(self, _to, _title, _body):
        if not self.smtp.is_connected():
            self.connect_smtp()
        self.smtp.send_message(_to, _title, _body)
        return self.accounts[self.index_account][0]


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