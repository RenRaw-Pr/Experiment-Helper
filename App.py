import os
import sys
import webbrowser
import customtkinter
import subprocess
from PIL import Image
from extensions import math_func as mf
from extensions import config_func as cf
from extensions import preprocess_func as pf
from typing import Union

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.params()
        self.find_center()
        self.title(f'| Experiment Helper v {self.CONFIG.sys_param("VERSION")} |')
        self.geometry(f"{self.APP_WIDTH}x{self.APP_HEIGHT}+{int(self.X_APP)}+{int(self.Y_APP)}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.put_main_frames()
        
        self.keyboard_bind()

    def params(self) -> None:
        self.CONFIG = cf.CONFIGURATION("../data_files/configuration.json")
        self.SESSION = cf.SESSION("../data_files/session.json")
        
        customtkinter.set_appearance_mode(self.CONFIG.get_param('theme'))
        customtkinter.set_default_color_theme(self.CONFIG.get_param('color_theme'))

        self.minsize(1060,550)
        self.APP_WIDTH = 1200
        self.APP_HEIGHT = 550

        self.OPT_WIDTH = 500
        self.OPT_HEIGHT = 500

        self.button_font = customtkinter.CTkFont(family="Square721 BT", size=12)
        self.info_font = customtkinter.CTkFont(family="Square721 BT", size=14)
        self.labels_font = customtkinter.CTkFont(family="Square721 BT", size=12)

        return 0
    
    def find_center(self) -> None:
        SCREEN_WIDTH = self.winfo_screenwidth()
        SCREEN_HEIGHT = self.winfo_screenheight()

        self.X_APP = (SCREEN_WIDTH / 2) - (self.APP_WIDTH / 2)
        self.Y_APP = (SCREEN_HEIGHT / 2) - (self.APP_HEIGHT / 2)

        self.X_OPT = (SCREEN_WIDTH / 2) - (self.OPT_WIDTH / 2)
        self.Y_OPT = (SCREEN_HEIGHT / 2) - (self.OPT_HEIGHT / 2)
        
        return None

    def put_main_frames(self) -> None:
        self.settings_bar = Settings_Bar(self)
        self.settings_bar.pack(fill='x')
        self.maintabview = Main_Tabview(self)
        self.maintabview.pack(fill='both', expand=True)
        self.dev_frame = Develop_frame(self)
        self.dev_frame.pack(padx=[0,0], pady=[1,1], fill='x')
        return None
    
    def on_closing(self, event=0) -> None:
        self.save_session()
        self.destroy()
        return None

    def keyboard_bind(self) -> None:
        self.bind('<Control-q>', lambda event : self.quit())
        return None

    def refresh_by_config(self) -> None:
        customtkinter.set_appearance_mode(self.CONFIG.get_param('theme'))
        customtkinter.set_default_color_theme(self.CONFIG.get_param('color_theme'))
        self.save_session()
        for child in self.winfo_children(): child.destroy()
        self.put_main_frames()
        return None
    
    def save_session(self) -> None:
        self.SESSION.set_param(tab='tab_0', key='_data_0', new_value=self.maintabview.INFOBAR.get_data(self.CONFIG.get_param("multiplicity")))
        self.SESSION.set_param(tab='tab_0', key='_formula_0', new_value=self.maintabview.basic_formula_entry.get("0.0", "end").replace('\n', ''))
        return None

    def update_tab(self) -> None:
        self.bufer_label = customtkinter.CTkLabel(self, height=1, width=1, text='')
        self.bufer_label.pack()
        self.after(2, lambda: self.bufer_label.destroy())
        return None

class Settings_Bar(customtkinter.CTkFrame):
    def __init__(self, master,
                 height: Union[int, float]=35,
                 corner_radius: Union[int, float]=0):
        super().__init__(master, height=height, corner_radius=corner_radius)
        self.opt = None

        self.settings_button = customtkinter.CTkButton(self, height=25,
                                                      text='Settings',
                                                      font=self.master.button_font,
                                                      command=lambda: self.settings())
        self.settings_button.pack(padx=[5,0], pady=[5,5], side='left')

        self.github_img = customtkinter.CTkImage(dark_image=Image.open(resource_path("./assets/github_light_mark.png")),
                                                 light_image=Image.open(resource_path("./assets/github_light_mark.png")),
                                                 size=(17, 17))

        self.github_button = customtkinter.CTkButton(self, height=25, width=25,
                                                    text="GitHub", font=self.master.button_font,
                                                    image=self.github_img, compound='right',
                                                    round_height_to_even_numbers=False,
                                                    round_width_to_even_numbers=False,
                                                    command=lambda:webbrowser.open_new("https://github.com/RenRaw-Pr/Experiment-Helper.git"))
        self.github_button.pack(padx=[5,5], pady=[5,5], side='right')

    def settings(self):
        if self.opt is None or not self.opt.winfo_exists():
            self.master.attributes('-fullscreen', False)
            self.opt = Settings_window(self.master)
            self.opt.attributes('-topmost', True)
            self.opt.focus()
        else:
            self.opt.focus()

# --------- FOR TAB 0
class Main_Tabview(customtkinter.CTkTabview):
    def __init__(self, master,
                 corner_radius: Union[int, float]=4):
        super().__init__(master, corner_radius=corner_radius, command=lambda: self.master.update_tab())
        self.__tabnames = {0: "| Indirect error |",
                           1: "| Сравнение на линейной шкале |",
                           2: "| Построение графиков |",
                           3: "| Instruction |"}
        
        self._segmented_button.configure(font=self.master.button_font)
        self.add(self.__tabnames[0])
        self.fill_tab_0()


        #self.add(self.__tabnames[1])
        #self.fill_tab_1()

        #self.add(self.__tabnames[2])
        #self.fill_tab_2()

        self.add(self.__tabnames[3])
        self.fill_tab_3()
    
    def fill_tab_0(self) -> None:
        self.get_data_0(upd_type='ses')
        self.INFOBAR = Table_Infobar(self.tab(self.__tabnames[0]), width=400)
        self.INFOBAR.pack(padx=[0,5], pady=[0,0], side='left', fill='both')
        self.INFOBAR.insert(self._data_0, self.master.CONFIG.get_param("number_format"))

        self.FORMULA_FRAME = customtkinter.CTkFrame(self.tab(self.__tabnames[0]))
        self.FORMULA_FRAME.pack(padx=[0,5], pady=[0,0], side='left', fill='both', expand=True)

        self.basic_formula_label = customtkinter.CTkLabel(self.FORMULA_FRAME,
                                                    height=25, width=310,
                                                    corner_radius=5,
                                                    text="Input formula like in Python3.10:",
                                                    justify='left',
                                                    font=self.master.info_font)
        self.basic_formula_label.pack(padx=[5,5], pady=[5,0], anchor='w', fill='x')

        self.basic_formula_entry = customtkinter.CTkTextbox(self.FORMULA_FRAME,
                                                            width=310,
                                                            corner_radius=5,
                                                            wrap='char', font=self.master.info_font)
        self.basic_formula_entry.pack(padx=[5,5], pady=[5,5], anchor='nw', fill='x', expand=True)
        self.basic_formula_entry.insert("0.0", str(self._formula_0))

        self.RESULT_FRAME = customtkinter.CTkFrame(self.tab(self.__tabnames[0]))
        self.RESULT_FRAME.pack(padx=[0,0], pady=[0,0], side='left', fill='y')

        self.start_process_button = customtkinter.CTkButton(self.RESULT_FRAME,
                                                            height=25, width=300, 
                                                            corner_radius=5,
                                                            text='= Calculate',
                                                            font=self.master.button_font,
                                                            command=lambda: self.display_result_tab_0())
        self.start_process_button.pack(padx=[5,5], pady=[5,0], anchor='nw', fill='x')

        self.result_frame = customtkinter.CTkFrame(self.RESULT_FRAME,
                                                            width=300,
                                                            corner_radius=5)
        self.result_frame.pack(padx=[5,5], pady=[5,5], anchor='nw', fill='both', expand=True)
        if self._data_0!={} and self._formula_0!="":
            self.display_result_tab_0()
        return None

    def fill_tab_1(self) -> None:
        return None
    
    def fill_tab_2(self) -> None:
        return None

    def fill_tab_3(self) -> None:
        self.INSTRUCTION = customtkinter.CTkTextbox(self.tab(self.__tabnames[3]), font=self.master.info_font, wrap='word')
        self.INSTRUCTION.insert('0.0', ''.join(open(resource_path('data_files/instruction.txt'), encoding='utf-8').readlines()))
        self.INSTRUCTION.pack(fill='both',expand=True)
        return None
    
    def get_data_0(self, upd_type: str='upd') -> None:
        if upd_type=='upd':
            self._data_0 = self.INFOBAR.get_data(self.master.CONFIG.get_param("multiplicity"))
            self._formula_0 = self.basic_formula_entry.get("0.0", "end")
        if upd_type=='ses':
            self._data_0 = self.master.SESSION.get_param('tab_0', '_data_0')
            self._formula_0 = self.master.SESSION.get_param('tab_0', '_formula_0')
        return None

    def calculate_0(self) -> None:
        self._function_value_0, self._data_0 = mf.transform_data(self._formula_0, self._data_0)
        self._summ_error_0, self._data_0 = mf.count_summ_error(self._data_0)
        return None
    
    def display_result_tab_0(self) -> None:
        for child in self.result_frame.winfo_children(): child.destroy()
        
        self.get_data_0()
        self.calculate_0()

        self.VALUE_FRAME = customtkinter.CTkFrame(self.result_frame, fg_color='transparent',)
        self.VALUE_FRAME.pack(padx=[5,5], pady=[5,0], anchor='nw', fill='x')

        self.label_1 = customtkinter.CTkLabel(self.VALUE_FRAME,
                                                  anchor='nw', justify='left',
                                                  text="Expression value:",
                                                  font=self.master.info_font)
        self.label_1.pack(padx=[2.5,2.5], pady=[0,0], side='left', anchor='nw')
        
        self.value_label = customtkinter.CTkLabel(self.VALUE_FRAME,
                                                  corner_radius=5,
                                                  anchor='ne', justify='right',
                                                  text=str(
                                                      mf.adjusted_scientific_notation(self._function_value_0, 
                                                                                     self.master.CONFIG.get_param("multiplicity"))[
                                                                                        self.master.CONFIG.get_param("number_format")]),
                                                  font=self.master.info_font)
        self.value_label.pack(padx=[2.5,2.5], pady=[0,0], side='right', anchor='ne')
        
        self.ERROR_FRAME = customtkinter.CTkFrame(self.result_frame, fg_color='transparent')
        self.ERROR_FRAME.pack(padx=[5,5], pady=[0,0], anchor='nw', fill='x')
        
        self.label_2 = customtkinter.CTkLabel(self.ERROR_FRAME,
                                                  anchor='nw', justify='left',
                                                  text="Error value:",
                                                  font=self.master.info_font)
        self.label_2.pack(padx=[2.5,2.5], pady=[0,0], side='left', anchor='nw')

        self.error_label = customtkinter.CTkLabel(self.ERROR_FRAME,
                                                  anchor='ne', justify='left',
                                                  text=str(
                                                      mf.adjusted_scientific_notation(self._summ_error_0, 
                                                                                     self.master.CONFIG.get_param("multiplicity"))[
                                                                                        self.master.CONFIG.get_param("number_format")]),
                                                  font=self.master.info_font)
        self.error_label.pack(padx=[2.5,2.5], pady=[0,0], side='right', anchor='ne')

        self.delimeter = customtkinter.CTkProgressBar(self.result_frame,
                                                      orientation="horizontal",
                                                      height=5)
        self.delimeter.set(1)
        self.delimeter.pack(padx=[5,5], pady=[0,0], anchor='nw', fill='x')

        self.percent_label = customtkinter.CTkLabel(self.result_frame,
                                                    anchor='nw', justify='left',
                                                    text="The error of each variable \nand its contribution to the total error:",
                                                    font=self.master.labels_font)
        self.percent_label.pack(padx=[5,5], pady=[5,0], anchor='nw', fill='x')

        self.PERCENT_FRAME = customtkinter.CTkScrollableFrame(self.result_frame)
        self.PERCENT_FRAME.pack(padx=[5,5], pady=[5,5], anchor='nw', fill='both', expand=True)

        self.PERCENT_FRAME.columnconfigure(0, weight=2)
        self.PERCENT_FRAME.columnconfigure(1, weight=2)
        for i, key in enumerate(self._data_0.keys()):

            self.var_name = customtkinter.CTkLabel(self.PERCENT_FRAME,
                                                   anchor='nw', justify='left',
                                                   text=key,
                                                   font=self.master.info_font)
            self.var_name.grid(row=i, column=0, padx=[2.5, 2.5], pady=[2.5, 2.5], sticky='NSEW')

            self.var_error = customtkinter.CTkLabel(self.PERCENT_FRAME,
                                                    anchor='ne', justify='right',
                                                    text=str(
                                                      mf.adjusted_scientific_notation(self._data_0[key][3], 
                                                                                     self.master.CONFIG.get_param("multiplicity"))[
                                                                                        self.master.CONFIG.get_param("number_format")]),
                                                    font=self.master.info_font)
            self.var_error.grid(row=i, column=1, padx=[2.5, 20], pady=[2.5, 2.5], sticky='NSEW')

            self.var_per = customtkinter.CTkLabel(self.PERCENT_FRAME,
                                                  anchor='ne', justify='right',
                                                  text=self._data_0[key][4],
                                                  font=self.master.info_font)
            self.var_per.grid(row=i, column=2, padx=[2.5, 2.5], pady=[2.5, 2.5], sticky='NSEW')

        return None
   
class Table_Infobar(customtkinter.CTkFrame):
    def __init__(self, master,
                 width: Union[int, float]=400,
                 corner_radius: Union[int, float]=5):
        super().__init__(master, width=width, corner_radius=corner_radius)
        self.font = customtkinter.CTkFont(family="Square721 BT", size=12)
        
        self.add_row_button = customtkinter.CTkButton(self, height=25, width=width,
                                                      text='+ Add variable', font=self.font,
                                                      command=lambda:self.add_row())
        self.add_row_button.pack(padx=[5,5], pady=[5,0], fill='x')

        self.table = customtkinter.CTkScrollableFrame(self)
        self.table.pack(padx=[5,5], pady=[5,5], fill='both', expand=True)

        self._rows = []

    def add_row(self) -> None:
        self._rows.append(Variable_row(self.table))
        for i, elem in enumerate(self._rows):
            elem.grid(row=i, column=0, padx=[0,0], pady=[0,0])
        return None
     
    def get_data(self, degree_round: int='3') -> dict:
        self._data = {}
        for elem in self._rows:
            if elem.name_entry.get()!='':
                self._data[elem.name_entry.get()] = [
                    mf.adjusted_scientific_notation(pf.convert_from_entry(elem.value_entry.get()), int(degree_round)),
                    mf.adjusted_scientific_notation(pf.convert_from_entry(elem.error_entry.get()), int(degree_round))
                    ]
        return self._data
    
    def insert(self, data: dict, number_format: str="Scientific") -> None:
        self._data = data
        for i, key in enumerate(self._data.keys()):
            self.add_row()
            self._rows[i].name_entry.insert(0, key)
            self._rows[i].value_entry.insert(0, self._data[key][0][number_format])
            self._rows[i].error_entry.insert(0, self._data[key][1][number_format])
        return None

class Variable_row(customtkinter.CTkFrame): 
    def __init__(self, master,
                 height: Union[int, float]=40,
                 width: Union[int, float]=400,
                 corner_radius: Union[int, float]=5):
        super().__init__(master, height=height, width=width, corner_radius=corner_radius)
        self.font = customtkinter.CTkFont(family="Square721 BT", size=14)
        self.delete_button = customtkinter.CTkButton(self, height=25, width=25,
                                                      text='X', font=self.font,
                                                      command=lambda:self.delete_self())
        self.delete_button.pack(padx=[0, 0], pady=[2.5, 2.5], side='left')

        self.name_entry = customtkinter.CTkEntry(self, height=25, width=60, 
                                                 placeholder_text="Name", font=self.font)
        self.name_entry.pack(padx=[2.5, 0], pady=[2.5, 2.5], side='left', fill='x', expand=True)

        self.value_entry = customtkinter.CTkEntry(self, height=25, width=140, 
                                                 placeholder_text="Value", font=self.font,
                                                 validate='key',
                                                 validatecommand=(self.register(pf.validate_command), "%P"))
        self.value_entry.pack(padx=[2.5, 0], pady=[2.5, 2.5], side='left', fill='x', expand=True)

        self.error_entry = customtkinter.CTkEntry(self, height=25, width=140, 
                                                 placeholder_text="Error", font=self.font,
                                                 validate='key',
                                                 validatecommand=(self.register(pf.validate_command), "%P"))
        self.error_entry.pack(padx=[2.5, 0], pady=[2.5, 2.5], side='left', fill='x', expand=True)
    
    def delete_self(self) -> None:
        self.master.master.master.master._rows.remove(self)
        self.destroy()
# ---------

class Develop_frame(customtkinter.CTkFrame): 
    def __init__(self, master,
                 height: Union[int, float]=10,
                 corner_radius: Union[int, float]=0):
        super().__init__(master, height=height, corner_radius=corner_radius)
        self.label_1 = customtkinter.CTkLabel(self,
                                            height=8,
                                            corner_radius=corner_radius,
                                            text=f"Version : {self.master.CONFIG.sys_param('VERSION')}",
                                            anchor='e', 
                                            font=customtkinter.CTkFont(family="Square721 BT", size=8))
        self.label_1.pack(padx=[2,2], pady=[2,2], side='right')
        
        self.label_2 = customtkinter.CTkLabel(self,
                                            height=8,
                                            corner_radius=corner_radius,
                                            text=f"Application path: {sys.argv[0]}  ",
                                            anchor='e', 
                                            font=customtkinter.CTkFont(family="Square721 BT", size=8))
        self.label_2.pack(padx=[2,2], pady=[2,2], side='right')
        self.label_2.bind("<Button-1>", lambda e: self.__open_dir())

        self.label_3 = customtkinter.CTkLabel(self,
                                            height=8,
                                            corner_radius=corner_radius,
                                            text=f"Release datetime : {self.master.CONFIG.sys_param('DATE')}",
                                            anchor='e', 
                                            font=customtkinter.CTkFont(family="Square721 BT", size=8))
        self.label_3.pack(padx=[2,2], pady=[2,2], side='right')
    
    def __open_dir(self) -> None:
        if os.path.exists(sys.argv[0]):
            subprocess.call(["open", "-R", sys.argv[0]])
        return None

class Settings_window(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('| Settings |')
        self.geometry(f"{master.OPT_WIDTH}x{master.OPT_HEIGHT}+{int(master.X_OPT)}+{int(master.Y_OPT)}")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.deiconify()
        
        self.button_font = customtkinter.CTkFont(family="Square721 BT", size=12)
        self.label_font = customtkinter.CTkFont(family="Square721 BT", size=12)

        self.frame_left = customtkinter.CTkFrame(self,
                                                width=(master.OPT_WIDTH-30)/2,
                                                height=master.OPT_HEIGHT-20,
                                                corner_radius=10)
        self.frame_left.pack(padx=[10,5], pady=10, side='left', fill='both')
        
        self.frame_right = customtkinter.CTkFrame(self,
                                                width=(master.OPT_WIDTH-30)/2,
                                                height=master.OPT_HEIGHT-100,
                                                corner_radius=10)
        self.frame_right.pack(padx=[5,10], pady=[10,0], side='top', fill='both', expand=True)

        self.frame_save = customtkinter.CTkFrame(self,
                                                width=(master.OPT_WIDTH-30)/2,
                                                height=30,
                                                corner_radius=10)
        self.frame_save.pack(padx=[5,10], pady=[0,10], side='bottom', fill='both')

        self.save_button = customtkinter.CTkButton(self.frame_save, 
                                                    width=(master.OPT_WIDTH-30)/2-10, 
                                                    height=20,
                                                    text="SAVE SETTINGS",
                                                    font=self.button_font,
                                                    command=lambda: self.save_button_function())
        self.save_button.pack(padx=5, pady=5)

        self.frame_default = customtkinter.CTkFrame(self,
                                                    width=(master.OPT_WIDTH-30)/2,
                                                    height=30,
                                                    corner_radius=10)
        self.frame_default.pack(padx=[5,10], pady=[5,10], side='bottom', fill='both')

        self.default_button = customtkinter.CTkButton(self.frame_default, 
                                                    width=(master.OPT_WIDTH-30)/2-10, 
                                                    height=20,
                                                    text="RESET SETTINGS",
                                                    font=self.button_font,
                                                    command=lambda: self.default_button_func())
        self.default_button.pack(padx=5, pady=5)

        self.label_1l = customtkinter.CTkLabel(self.frame_left,
                                                width=(master.OPT_WIDTH-30)/2-20,
                                                height=20,
                                                text="Number format:",
                                                anchor='w',
                                                font=self.label_font)
        self.label_1l.pack(padx=[5,5], pady=[5,5])

        self.optionmenu_1l = customtkinter.CTkOptionMenu(self.frame_left,
                                                        width=(master.OPT_WIDTH-30)/2-20,
                                                        height=25,
                                                        values=cf.mix_values(["Scientific", "Classical"],
                                                                                self.master.CONFIG.get_param('number_format')),
                                                        font=self.button_font)
        self.optionmenu_1l.pack(padx=[5,5], pady=[5,5])

        self.label_2l = customtkinter.CTkLabel(self.frame_left,
                                                width=(master.OPT_WIDTH-30)/2-20,
                                                height=20,
                                                text="Multiplicity of degrees:",
                                                anchor='w',
                                                font=self.label_font)
        self.label_2l.pack(padx=[5,5], pady=[5,5])

        self.optionmenu_2l = customtkinter.CTkOptionMenu(self.frame_left,
                                                        width=(master.OPT_WIDTH-30)/2-20,
                                                        height=25,
                                                        values=list(map(str, cf.mix_values([3, 5],
                                                                            self.master.CONFIG.get_param('multiplicity')))),
                                                        font=self.button_font)
        self.optionmenu_2l.pack(padx=[5,5], pady=[5,5])

        self.label_1r = customtkinter.CTkLabel(self.frame_right,
                                                width=(master.OPT_WIDTH-30)/2-20,
                                                height=20,
                                                text="Theme:",
                                                anchor='w',
                                                font=self.label_font)
        self.label_1r.pack(padx=[5,5], pady=[5,5])
        
        self.optionmenu_1r = customtkinter.CTkOptionMenu(self.frame_right,
                                                        width=(master.OPT_WIDTH-30)/2-20,
                                                        height=25,
                                                        values=cf.mix_values(["Dark", "Light"],
                                                                                self.master.CONFIG.get_param('theme')),
                                                        font=self.button_font)
        self.optionmenu_1r.pack(padx=[5,5], pady=[5,5])

        self.label_2r = customtkinter.CTkLabel(self.frame_right,
                                                width=(master.OPT_WIDTH-30)/2-20,
                                                height=20,
                                                text="Color theme:",
                                                anchor='w',
                                                font=self.label_font)
        self.label_2r.pack(padx=[5,5], pady=[5,5])

        self.optionmenu_2r = customtkinter.CTkOptionMenu(self.frame_right,
                                                        width=(master.OPT_WIDTH-30)/2-20,
                                                        height=25,
                                                        values=cf.mix_values(["blue", "dark-blue", "green"],
                                                                                self.master.CONFIG.get_param('color_theme')),
                                                        font=self.button_font)
        self.optionmenu_2r.pack(padx=[5,5], pady=[5,5])
        
        self.keyboard_bind()

    def save_button_function(self) -> None:
        self.master.CONFIG.set_param('number_format', self.optionmenu_1l.get())
        self.master.CONFIG.set_param('multiplicity', int(self.optionmenu_2l.get()))
        self.master.CONFIG.set_param('theme', self.optionmenu_1r.get())
        self.master.CONFIG.set_param('color_theme', self.optionmenu_2r.get())
        self.master.refresh_by_config()
        self.__on_closing()
        return None

    def default_button_func(self) -> None:
        self.master.CONFIG.return_to_default()
        self.master.refresh_by_config()
        self.__on_closing()
        return None

    def keyboard_bind(self) -> None:
        self.bind('<Control-d>', lambda event : self.default_button_func())
        self.bind('<Control-q>', lambda event : self.on_closing())
        return None

    def __on_closing(self, event=0) -> None:
        self.master.focus_force()
        self.destroy()
        return None

if __name__ == "__main__":
    app = App()
    app.mainloop()