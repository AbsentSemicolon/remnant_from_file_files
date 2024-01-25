'''
    For configuration of remnant: from the files
'''

import configparser
import re

GENERAL = 'GENERAL'
STEAM = 'STEAM'

class RemConfig():
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read('./config.ini')

    def __is_true(self, value)-> bool:
        return bool(value.upper() in ['TRUE'])

    def get_config(self) -> list:
        return self.config.read('config.ini')

    def get_steam_id(self) -> str:
        return self.config[STEAM]['SteamUserId']

    def get_take_backups(self) -> bool:
        return self.__is_true(self.config[GENERAL]['TakeBackups'])

    def get_test_imp(self) -> bool:
        return self.__is_true(self.config[GENERAL]['TestImplementation'])

    def validate_config(self) -> bool:
        try:
            steam_id = self.get_steam_id()

            if re.match(r'^[0-9]{1,16}$', steam_id) == None:
                return False

        except:
            print('There was an error validating config.')

        return True
