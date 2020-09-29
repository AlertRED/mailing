from model.MailingModel import MailingModel
from model.XlsxModel import XlsxModel
from settings import Settings


class MainDao:

    def __init__(self, model_mailing: MailingModel, xlsx_model: XlsxModel, controller, settings: Settings):
        self.model_mailing = model_mailing
        self.xlsx_model = xlsx_model
        self.controller = controller
        self.settings = settings
        self.is_pause = False
        self.is_start = False

    def openDataWindow(self):
        self.controller.dataView.show()

    def openAccountsWindow(self):
        self.controller.accountsView.show()

    def pause_mailing(self):
        self.model_mailing.pause_mailing()

    def stop_mailing(self):
        self.model_mailing.stop_mailing()

    def mailing(self):
        message = self.settings.get_settings('message')
        email_title = self.settings.get_settings('email_column')
        return self.model_mailing.start_mailing(self.xlsx_model.titles, message, self.xlsx_model.fields, email_title)


