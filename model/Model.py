import re
from time import sleep

import pandas as pd
import json
import os


class Model:

    def __init__(self):
        self.accounts = list()
        self.message = str()
        self.emails = list()
        self.fields = dict()
        self.xlsx_data = None
        self.file = None
        self.email_column = ''

        self.is_pause = False
        self.is_start = False

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
                    if len(account) == 2 and self.is_validate_password(account[0]) and self.is_validate_email(
                            account[0]):
                        self.accounts.append(tuple(account))
                else:
                    break

    def save_settings(self, window_name: str, settings: dict):


        self.path_xlsx = settings.get('path_xlsx')
        self.sheet = settings.get('sheet')
        self.email_column = settings.get('email_column')
        self.message = settings.get('message')
        self.is_single = settings.get('is_single')
        self.email = settings.get('email')
        self.password = settings.get('password')
        self.path_txt = settings.get('path_txt')
        self.email_index = settings.get('email_index')


        with open('settings.json', 'r+') as file:
            json_settings = json.load(file)

        json_settings[window_name] = settings

        with open('settings.json', 'w') as file:
            json.dump(json_settings, file)

    def get_settings(self, window_name: str):
        with open('settings.json', 'r+') as file:
            try:
                return json.load(file).get(window_name, dict())
            except:
                return dict()

    def getCountAccounts(self):
        return len(self.accounts)

    def load_xlsx(self, path):
        _, file_extension = os.path.splitext(path)
        if file_extension == '.xlsx' and os.path.isfile(path):
            self.file = pd.ExcelFile(path)
        else:
            self.file = None
        # self.xlsx_data = self.xlsx_data.fillna('')

    def get_sheets(self):
        if self.file:
            return self.file.sheet_names
        return []

    def get_data_from_sheet(self, sheet):
        return self.file.parse(sheet, dtype=str).fillna('')

    def set_email_column(self, text: str):
        self.email_column = text

    def pause_mailing(self):
        self.is_pause = True

    def stop_mailing(self):
        self.is_start = False
        self.is_pause = False
        self.save_settings('Main', {'email_index': 0})

    def mailing(self):
        if not self.is_start or self.is_pause:
            self.is_start = True
            self.is_pause = False
            start_index = self.get_settings('Main').get('email_index', 0)
            for i in range(start_index, 5):
                if not self.is_start or self.is_pause:
                    break
                email = f'{i}@mail.ru'
                self.save_settings('Main', {'email_index': i + 1})
                yield email
                sleep(1)