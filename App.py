import os
import sys
import customtkinter
from extensions import math_func as mf
from typing import Union

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.params()
        self.find_center()
        self.title(f'| Prac. tool v {self.VERSION} |')
        self.geometry(f"{self.APP_WIDTH}x{self.APP_HEIGHT}+{int(self.X_APP)}+{int(self.Y_APP)}")
        self.minsize(920,550)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.put_main_frames()
        
        self.keyboard_bind()

    def params(self) -> None:
        customtkinter.set_appearance_mode('Dark')
        customtkinter.set_default_color_theme('blue')
        self.VERSION = '0.0.0.1'
        self.APP_WIDTH = 1015
        self.APP_HEIGHT = 550

        self.button_font = customtkinter.CTkFont(family="Square721 BT", size=12)
        self.info_font = customtkinter.CTkFont(family="Square721 BT", size=14)
        self.labels_font = customtkinter.CTkFont(family="Square721 BT", size=12)

        return 0
    
    def find_center(self) -> None:
        SCREEN_WIDTH = self.winfo_screenwidth()
        SCREEN_HEIGHT = self.winfo_screenheight()

        self.X_APP = (SCREEN_WIDTH / 2) - (self.APP_WIDTH / 2)
        self.Y_APP = (SCREEN_HEIGHT / 2) - (self.APP_HEIGHT / 2)
        
        return None

    def put_main_frames(self) -> None:
        #self.option_bar = 
        self.maintabview = Main_Tabview(self)
        self.maintabview.pack(fill='both', expand=True)
        return None
    
    def on_closing(self, event=0) -> None:
        self.destroy()
        return None

    def keyboard_bind(self) -> None:
        self.bind('<Control-q>', lambda event : self.quit())
        return None

    def update_tab(self) -> None:
        self.bufer_label = customtkinter.CTkLabel(self, height=1, width=1, text='')
        self.bufer_label.pack()
        self.after(2, lambda: self.bufer_label.destroy())
        return None
    
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
        self.INFOBAR = Table_Infobar(self.tab(self.__tabnames[0]))
        self.INFOBAR.pack(padx=[0,5], pady=[0,0], side='left', fill='both', expand=True)

        self.FORMULA_FRAME = customtkinter.CTkFrame(self.tab(self.__tabnames[0]))
        self.FORMULA_FRAME.pack(padx=[0,5], pady=[0,0], side='left', fill='y')

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
        self.basic_formula_entry.pack(padx=[5,5], pady=[5,5], anchor='nw')

        self.RESULT_FRAME = customtkinter.CTkFrame(self.tab(self.__tabnames[0]))
        self.RESULT_FRAME.pack(padx=[0,0], pady=[0,0], side='left', fill='y')

        self.start_process_button = customtkinter.CTkButton(self.RESULT_FRAME,
                                                            height=25, width=300, 
                                                            corner_radius=5,
                                                            text='= Calculate',
                                                            font=self.master.button_font,
                                                            command=lambda: self.get_data_0())
        self.start_process_button.pack(padx=[5,5], pady=[5,0], anchor='nw', fill='x')

        self.result_frame = customtkinter.CTkFrame(self.RESULT_FRAME,
                                                            width=300,
                                                            corner_radius=5)
        self.result_frame.pack(padx=[5,5], pady=[5,5], anchor='nw', fill='both', expand=True)
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
    
    def get_data_0(self) -> None:
        self._data_0 = self.INFOBAR.get_data()
        self._function_value, self._data_0 = mf.transform_data(self.basic_formula_entry.get("0.0", "end"), self._data_0)
        self._summ_error, self._data_0 = mf.count_summ_error(self._data_0)
        self._function_value, self._summ_error = mf.round_by_error(self._function_value, self._summ_error)
        
        self.update_result_tab_0()
        return None
    
    def update_result_tab_0(self) -> None:
        for child in self.result_frame.winfo_children(): child.destroy()
        
        self.VALUE_FRAME = customtkinter.CTkFrame(self.result_frame, fg_color='transparent',)
        self.VALUE_FRAME.pack(padx=[5,5], pady=[5,0], anchor='nw', fill='x')

        self.label_1 = customtkinter.CTkLabel(self.VALUE_FRAME,
                                                  anchor='nw', justify='left',
                                                  text="Expression value:",
                                                  font=self.master.info_font)
        self.label_1.pack(padx=[2.5,2.5], pady=[0,0], side='left', anchor='nw')
        
        self.value_label = customtkinter.CTkLabel(self.VALUE_FRAME,
                                                  corner_radius=5,
                                                  anchor='nw', justify='left',
                                                  text=str(self._function_value),
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
                                                  anchor='nw', justify='left',
                                                  text=str(self._summ_error),
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
                                                    anchor='nw', justify='right',
                                                   text=str(mf.round_by_meaning(self._data_0[key][3])),
                                                   font=self.master.info_font)
            self.var_error.grid(row=i, column=1, padx=[2.5, 2.5], pady=[2.5, 2.5], sticky='NSEW')

            self.var_per = customtkinter.CTkLabel(self.PERCENT_FRAME,
                                                  anchor='nw', justify='right',
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
        
        self.add_row_button = customtkinter.CTkButton(self, height=25, width=60,
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
     
    def get_data(self) -> dict:
        self._data = {}
        for elem in self._rows:
            self._data[elem.name_entry.get()] = [float(elem.value_entry.get().replace(',', '.')), float(elem.error_entry.get().replace(',', '.'))]
        return self._data

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

        self.value_entry = customtkinter.CTkEntry(self, height=25, width=120, 
                                                 placeholder_text="Value", font=self.font)
        self.value_entry.pack(padx=[2.5, 0], pady=[2.5, 2.5], side='left', fill='x', expand=True)

        self.error_entry = customtkinter.CTkEntry(self, height=25, width=120, 
                                                 placeholder_text="Error", font=self.font)
        self.error_entry.pack(padx=[2.5, 0], pady=[2.5, 2.5], side='left', fill='x', expand=True)

    def delete_self(self) -> None:
        self.master.master.master.master._rows.remove(self)
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()