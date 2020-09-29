import re
from time import sleep

import pandas as pd
import json
import os


class ValidateModel:

    def __init__(self):
        pass

    def is_validate_email(self, email):
        return re.match(r'[^@]+@[^@]+\.[^@]+', email)

    def is_validate_password(self, password):
        return password != ''

    def is_validate_xlsx(self, path):
        _, file_extension = os.path.splitext(path)
        return file_extension == '.xlsx' and os.path.isfile(path)






