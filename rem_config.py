'''
    For configuration of remnant: from the files
'''

import configparser
import re

class RemConfig():
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read('./config.ini')

    def get_config(self):
        return self.config.read('config.ini')

    def get_steam_id(self):
        return self.config['STEAM']['SteamUserId']

    def validate_config(self):
        try:
            steam_id = self.get_steam_id()

            if re.match(r'^[0-9]{1,16}$', steam_id) == None:
                return False

        except:
            print('There was an error validating config.')


        return True
