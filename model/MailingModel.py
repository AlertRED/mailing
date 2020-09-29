from time import sleep

from settings import Settings


class MailingModel:

    def __init__(self, settings: Settings):
        self.is_pause = False
        self.is_start = False
        self.settings = settings
        self.iter_list_info = None

    def pause_mailing(self):
        self.is_pause = True

    def stop_mailing(self):
        self.is_start = False
        self.is_pause = False
        self.settings.add_settings({'email_index': 0})

    def start_mailing(self, headers, message, fields, emile_title):
        if not self.is_start or self.is_pause:
            self.is_start = True
            self.is_pause = False
            start_index = self.settings.get_settings('email_index', 0)
            return self.mailing(start_index, fields, headers, message, emile_title)

    def mailing(self, start_index, list_info, headers: list, message_format, email_title):
        email_index = headers.index(email_title)
        for i, row in enumerate(list_info):
            if not self.is_start or self.is_pause:
                break

            message = f'To: {row[email_index]}\n'
            args = dict()
            for i, header in enumerate(headers):
                args[header] = row[i]
            message += 'Message: ' + message_format.format(**args)
            yield str(message)
            self.settings.add_settings({'email_index': i + 1})
            sleep(1)
