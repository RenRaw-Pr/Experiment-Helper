import json
import os
import sys
from typing import Any, Union

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class CONFIGURATION():
    def __init__(self, path: str='../data_files/configuration.json'):
        self.__path = resource_path(path)
        if not os.path.exists(self.__path):
            self.__create()
        self.__file = open(self.__path, mode='r', encoding='utf-8')
        try:
            self.__data = json.load(self.__file)
        except json.decoder.JSONDecodeError:
            self.__file.close()
            os.remove(self.__path)
            self.__create()
            self.__file = open(self.__path, mode='r', encoding='utf-8')
            self.__data = json.load(self.__file)
        self.__file.close()

    def __create(self) -> None:
        self.__data = {'SYSTEM_DATA' : {'VERSION' : '0.0.0.3',
                                      'DATE' : '2023-22-12'},
                     'DEFAULT_SETTINGS' : {'theme' : 'Dark',
                                           'color_theme' : 'blue',
                                           'number_format' : 'Scientific',
                                           'multiplicity' : 3,
                                           'language' : 'EN',
                                           'font_family' : 'Apple Braille'},
                     'USER_SETTINGS' : {'theme' : 'Dark',
                                        'color_theme' : 'dark-blue',
                                        'number_format' : 'Scientific',
                                        'multiplicity' : 3,
                                        'language' : 'EN',
                                        'font_family' : 'Apple Braille'}}
        self.__write_to_file()
        return None
    
    def __write_to_file(self) -> None:
        with open(self.__path, mode='w', encoding='utf-8') as __session_file:
            json.dump(self.__data, __session_file, indent=2)

    def return_to_default(self) -> None:
        for key in self.__data['USER_SETTINGS'].keys():
            self.__data['USER_SETTINGS'][key] = self.__data['DEFAULT_SETTINGS'][key]
        self.__write_to_file()
        return None
    
    def get_param(self, key: str) -> Any:
        try: return self.__data['USER_SETTINGS'][key]
        except KeyError: return None

    def set_param(self, key: str, new_value: Any) -> bool:
        if key in self.__data["USER_SETTINGS"].keys():
            self.__data['USER_SETTINGS'][key] = new_value
            self.__write_to_file()
            return True
        else: return False
    
    def sys_param(self, key: str) -> Union[str, None]:
        try: return self.__data['SYSTEM_DATA'][key]
        except KeyError: return None
    
class SESSION():
    def __init__(self, path: str='../data_files/session.json'):
        self.__path = resource_path(path)
        if not os.path.exists(self.__path):
            self.__create()
        self.__file = open(self.__path, mode='r', encoding='utf-8')
        try:
            self.__data = json.load(self.__file)
        except json.decoder.JSONDecodeError:
            self.__file.close()
            os.remove(self.__path)
            self.__create()
            self.__file = open(self.__path, mode='r', encoding='utf-8')
            self.__data = json.load(self.__file)
        self.__file.close()

    def __create(self) -> None:
        self.__data = {'tab_0' : {
                            '_data_0' : {},
                            '_formula_0' : ""},
                       'tab_1' : {
                            '_data_1' : {}
                       },
                       'tab_2' : {},
                       'tab_3' : {}}
        self.__write_to_file()

    def __write_to_file(self) -> None:
        with open(self.__path, mode='w', encoding='utf-8') as __session_file:
            json.dump(self.__data, __session_file, indent=2)

    def get_param(self, tab: str, key: str) -> Any:
        try: return self.__data[tab][key]
        except KeyError: return None

    def set_param(self, tab: str, key: str, new_value: Any) -> bool:
        if key in self.__data[tab].keys():
            self.__data[tab][key] = new_value
            self.__write_to_file()
            return True
        else: return False

def mix_values(data: list, actual_value: Any) -> list:
    data.remove(actual_value)
    return [actual_value] + data