from rem_config import RemConfig
from print_statement import print_text, font_colors, font_types

from pathlib import Path
from os import path, listdir, stat
from collections import namedtuple
from time import sleep

from shutil import copyfile
from datetime import datetime

SaveFile = namedtuple('SaveFile', 'save_file_name, save_file_size')

class FilesNotFoundException(Exception):
    pass


class Remnant_File_Changer():
    file_errors = []

    def __init__(self) -> None:
        print("\033c", end='')
        print_text('\nRemnant: From the files\n', font_colors.HEADER, font_types.BOLD)
        print_text('This will copy files from Game Pass to Steam')
        print_text('and vice versa.')
        print_text('Please take care as this could mess up your saves.')
        print_text('\nWARNING: This will only change 1 save currently.\n', font_colors.WARNING)
        self.config = RemConfig()
        self.__validate_config()
        self.home = str(Path.home())
        self.steam_files = self.__find_steam_files()
        self.gamepass_files = self.__find_gamepass_files()
        self.__validate_files()

    def __find_steam_files(self) -> list:
        save_files = []
        steam_folder = f'{self.home}\\Saved Games\\Remnant2\\Steam\\{self.config.get_steam_id()}'

        try:
            if self.__folder_exists(steam_folder):
                # Hardcoding for first save and profile as these
                # are easy to asertain for Steam.
                # Profile is smaller so it'll always go first
                file_names = ['profile.sav', 'save_1.sav']

                for file in file_names:
                    save_files.append(
                        SaveFile(save_file_name=f'{steam_folder}\\{file}',
                                    save_file_size=stat(f'{steam_folder}\\{file}').st_size)
                                    )

                if len(save_files) == 0:
                    raise FilesNotFoundException()

                return save_files
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            self.file_errors.append(['Could not find the Steam folder for Remnant 2.', f'Check that {steam_folder} exists.'])
        except FilesNotFoundException:
            self.file_errors.append(['Could not locate files for Steam, check you have at least save_1.sav and profile.sav'])
        except Exception as error:
            print_text(error)
            exit()

        return save_files

    def __find_gamepass_files(self) -> list:
        # Navigate to Packages
        # Find the folder with PerfectWorld
        packages_segment = f'{self.home}\\AppData\\Local\\Packages\\'
        wgs_segment = '\\SystemAppData\\wgs'
        perfect_world_segment = 'PerfectWorldEntertainment.'
        save_folder = None
        save_folders = None
        save_files = []

        try:
            found_perfect_world = self.__find_folder(packages_segment, perfect_world_segment)
            all_segments = f'{packages_segment}{found_perfect_world}{wgs_segment}'
            for entry in listdir(all_segments):
                if path.isdir(path.join(all_segments, entry)):
                    if entry != 't':
                        save_folder = entry
                        break

            save_folders = f'{all_segments}\\{save_folder}'
            # Make tuple of folders with files and sizes
            # Lower value is profile
            # Higher value is save

            for entry in listdir(save_folders):
                if path.isdir(path.join(save_folders, entry)):
                    for file in listdir(f'{save_folders}\\{entry}'):
                        if 'container' not in file and '_' not in file:
                            file_loc = f'{save_folders}\\{entry}\\{file}'
                            save_files.append(
                                SaveFile(save_file_name=file_loc,
                                        save_file_size=stat(file_loc).st_size)
                                        )

            if len(save_files) == 0:
                raise FilesNotFoundException()

            # Sort the list to put profile first as should be the smallest
            save_files.sort(key=lambda x : x.save_file_size)
        except FileNotFoundError:
            self.file_errors.append(['Could not find the Game Pass folder for Remnant 2.', f'Check that {packages_segment}{perfect_world_segment}#######_#############{wgs_segment} exists.'])
        except FilesNotFoundException:
            self.file_errors.append(['Could not locate files for Game Pass, start the game and make at least one character.'])
        except Exception as error:
            print_text(error)
            exit()

        return save_files

    def __folder_exists(self, path_to_folder) -> bool:
        return path.exists(path_to_folder)

    def __find_folder(self, path_to_folder, folder) -> str:
        for entry in listdir(path_to_folder):
            if path.isdir(path.join(path_to_folder, entry)):
                if folder in entry:
                    return entry

        return None

    def __take_backups(self):
        if self.config.get_take_backups():
            print_text('Taking backups first', font_colors.OKGREEN)
            time = datetime.now().strftime('%Y%m%d%H%M%S')

            for file in self.steam_files:
                copyfile(file.save_file_name, f'{file.save_file_name}_bak_{time}')

            for file in self.gamepass_files:
                copyfile(file.save_file_name, f'{file.save_file_name}_bak_{time}')
        else:
            print_text('\nTEST: Taking backups first.', font_colors.OKGREEN)

    def __actually_move_files(self, source, dest):
        if self.config.get_test_imp():
            print_text('\nTEST: Copied files!', font_colors.OKGREEN)
        else:
            for (i, source_file) in enumerate(source):
                copyfile(source_file.save_file_name, dest[i].save_file_name)

    def __move_files(self, direction):
        new_direction = direction.upper()

        match new_direction:
            case 'S':
                self.__take_backups()
                print_text('Copying to Steam.')
                self.__actually_move_files(self.gamepass_files, self.steam_files)

            case 'G':
                self.__take_backups()
                print_text('Copying to Game Pass.')
                self.__actually_move_files(self.steam_files, self.gamepass_files)

            case 'Q':
                exit()

            case _:

                print_text('\nNothing was selected. Try again\n', font_colors.WARNING)
                self.start()

    # TODO: Figure out which files are newer
    def start(self):
        print_text('G to copy files to Game Pass')
        print_text('S to copy files to Steam')
        print_text('Q to quit')
        if self.config.get_test_imp():
            print_text('\nWARNING: Test mode activated.', font_colors.WARNING)
        direction = input('\nWhich direction do you want to go? ')
        self.__move_files(direction)

    def __validate_config(self):
        if self.config.validate_config() != True:
            print_text('\nThere was a problem validating configuration.\n')
            print_text('Please check the README.')
            exit()

    def __validate_files(self):
        if len(self.file_errors):
            for lines in self.file_errors:
                for line in lines:
                    print_text(line)
            exit()


if __name__ == '__main__':
    file_changer = Remnant_File_Changer()
    file_changer.start()