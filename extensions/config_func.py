import json
import os
import sys
from typing import Any, Union

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class CONFIGURATION():
    def __init__(self, path: str):
        self.path = resource_path(path)
        if not os.path.exists(self.path):
            self.__create()
        self.file = open(self.path, mode='r', encoding='utf-8')
        self.data = json.load(self.file)
        self.file.close()

    def __create(self) -> None:
        self.data = {'SYSTEM_DATA' : {'VERSION' : '0.0.0.2',
                                      'DATE' : '2023-09-12'},
                     'DEFAULT_SETTINGS' : {'theme' : 'Dark',
                                           'color_theme' : 'blue',
                                           'number_format' : 'Scientific'},
                     'USER_SETTINGS' : {'theme' : 'Dark',
                                        'color_theme' : 'green',
                                        'number_format' : 'Scientific'}}
        self.__write_to_file()
        return None
    
    def __write_to_file(self) -> None:
        with open(self.path, mode='w', encoding='utf-8') as session_file:
            json.dump(self.data, session_file, indent=4)

    def return_to_default(self) -> None:
        for key in self.data['USER_SETTINGS'].keys():
            self.data['USER_SETTINGS'][key] = self.data['DEFAULT_SETTINGS'][key]
        self.__write_to_file()
        return None
    
    def get_param(self, key: str) -> Union[str, None]:
        try: return self.data['USER_SETTINGS'][key]
        except KeyError: return None

    def set_param(self, key: str, new_value: str) -> bool:
        if key in self.data["USER_SETTINGS"].keys():
            self.data['USER_SETTINGS'][key] = new_value
            self.__write_to_file()
            return True
        else: return False
    
    def sys_param(self, key: str) -> Union[str, None]:
        try: return self.data['SYSTEM_DATA'][key]
        except KeyError: return None
    
class SESSION():
    def __init__(self, path: str):
        self.path = resource_path(path)
        if not os.path.exists(self.path):
            self.__create()
        self.file = open(self.path, mode='r', encoding='utf-8')
        self.data = json.load(self.file)
        self.file.close()

    def __create(self) -> None:
        self.data = {'tab_0' : {
                        '_data_0' : {},
                        '_formula_0' : ""},
                     'tab_1' : {},
                     'tab_2' : {},
                     'tab_3' : {}}
        self.__write_to_file()

    def __write_to_file(self) -> None:
        with open(self.path, mode='w', encoding='utf-8') as session_file:
            json.dump(self.data, session_file, indent=4)

    def get_param(self, tab: str, key: str) -> Union[str, None]:
        try: return self.data[tab][key]
        except KeyError: return None

    def set_param(self, tab: str, key: str, new_value: Any) -> bool:
        if key in self.data[tab].keys():
            self.data[tab][key] = new_value
            self.__write_to_file()
            return True
        else: return False
    
def mix_values(data: list, actual_value: Any) -> list:
    data.remove(actual_value)
    return [actual_value] + data