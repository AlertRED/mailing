from time import sleep


class MainDao:

    def __init__(self, model, controller):
        self.model = model
        self.controller = controller
        self.is_pause = False
        self.is_start = False

    def openDataWindow(self):
        self.controller.dataView.show()

    def openAccountsWindow(self):
        self.controller.accountsView.show()

    def pause_mailing(self):
        self.model.pause_mailing()

    def stop_mailing(self):
        self.model.stop_mailing()

    def mailing(self):
        return self.model.mailing()


