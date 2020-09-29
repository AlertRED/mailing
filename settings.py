import json


class Settings:
    def __init__(self):
        self.settings = dict()

    def add_settings(self, settings: dict):
        self.settings.update(settings)
        self.save_settings()

    def get_settings(self, key, default=None):
        return self.settings.get(key, default)

    def save_settings(self):
        with open('settings.json', 'w') as file:
            json.dump(self.settings, file)

    def load_settings(self):
        with open('settings.json', 'r+') as file:
            self.settings = json.load(file)
