import tkinter
import customtkinter
import math_func as mf
from typing import Union

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.params()
        self.find_center()
        self.title(f'| Prac. tool v {self.VERSION} |')
        self.geometry(f"{self.APP_WIDTH}x{self.APP_HEIGHT}+{int(self.X_APP)}+{int(self.Y_APP)}")
        self.minsize(865,550)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.put_main_frames()
        
        self.keyboard_bind()

    def params(self) -> None:
        customtkinter.set_appearance_mode('Dark')
        customtkinter.set_default_color_theme('blue')
        self.VERSION = '0.0.0.1'
        self.APP_WIDTH = 865
        self.APP_HEIGHT = 550

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

class Main_Tabview(customtkinter.CTkTabview):

    def __init__(self, master,
                 corner_radius: Union[int, float]=4):
        super().__init__(master, corner_radius=corner_radius)
        self.__tabnames = {0: "| Косвенная погрешность |",
                           1: "| Сравнение на линейной шкале |",
                           2: "| Построение графиков |"}
        self.add(self.__tabnames[0])
        self.fill_tab_0()

        #self.add(self.__tabnames[1])
        #self.fill_tab_1()

        #self.add(self.__tabnames[2])
        #self.fill_tab_2()
    
    def fill_tab_0(self) -> None:
        self.INFOBAR = Table_Infobar(self.tab(self.__tabnames[0]))
        self.INFOBAR.pack(padx=[0,5], pady=[0,0], side='left', fill='both', expand=True)

        self.FORMULA_FRAME = customtkinter.CTkFrame(self.tab(self.__tabnames[0]))
        self.FORMULA_FRAME.pack(padx=[0,5], pady=[0,0], side='left', fill='y')

        self.basic_formula_label = customtkinter.CTkLabel(self.FORMULA_FRAME,
                                                    height=25, width=310,
                                                    corner_radius=5,
                                                    text="Введите формулу в формате языка Python3.10:")
        self.basic_formula_label.pack(padx=[5,5], pady=[5,0], anchor='nw')

        self.basic_formula_entry = customtkinter.CTkTextbox(self.FORMULA_FRAME,
                                                            width=310,
                                                            corner_radius=5,
                                                            wrap='char')
        self.basic_formula_entry.pack(padx=[5,5], pady=[5,5], anchor='nw')
        '''
        self.latex_formula_label = customtkinter.CTkLabel(self.FORMULA_FRAME,
                                                    height=25,
                                                    corner_radius=5,
                                                    text="Введите формулу на языке LaTeX:")
        self.latex_formula_label.pack(padx=[5,5], pady=[5,0], anchor='nw')

        self.latex_formula_entry = customtkinter.CTkTextbox(self.FORMULA_FRAME,
                                                      corner_radius=5,
                                                      wrap='char')
        self.latex_formula_entry.pack(padx=[5,5], pady=[5,0], anchor='nw', fill='both', expand=True)

        self.res_label = customtkinter.CTkLabel(self.FORMULA_FRAME,
                                                    height=25,
                                                    corner_radius=5,
                                                    text="Визуализация формулы:")
        self.res_label.pack(padx=[5,5], pady=[5,0], anchor='nw')
        '''
        self.RESULT_FRAME = customtkinter.CTkFrame(self.tab(self.__tabnames[0]))
        self.RESULT_FRAME.pack(padx=[0,0], pady=[0,0], side='left', fill='y')

        self.start_process_button = customtkinter.CTkButton(self.RESULT_FRAME,
                                                            height=25, width=200, 
                                                            corner_radius=5,
                                                            text='Начать вычисления',
                                                            command=lambda: self.get_data())
        self.start_process_button.pack(padx=[5,5], pady=[5,0], anchor='nw', fill='x')

        self.result_textbox = customtkinter.CTkTextbox(self.RESULT_FRAME,
                                                            width=200,
                                                            corner_radius=5,
                                                            wrap='char')
        self.result_textbox.pack(padx=[5,5], pady=[5,5], anchor='nw')
        return None

    def fill_tab_1(self) -> None:
        return None
    
    def fill_tab_2(self) -> None:
        return None

    def get_data(self) -> None:
        self._data_0 = self.INFOBAR.get_data()
        self._function_value, self._data_0 = mf.transform_data(self.basic_formula_entry.get("0.0", "end"), self._data_0)
        self._summ_error, self._data_0 = mf.count_summ_error(self._data_0)
        print(self._function_value, self._summ_error, self._data_0)
    
class Table_Infobar(customtkinter.CTkFrame):

    def __init__(self, master,
                 width: Union[int, float]=400,
                 corner_radius: Union[int, float]=5):
        super().__init__(master, width=width, corner_radius=corner_radius)

        self.add_row_button = customtkinter.CTkButton(self, height=25, width=60,
                                                      text='|+| Добавить переменную',
                                                      command=lambda:self.add_row())
        self.add_row_button.pack(padx=[5,5], pady=[5,0], fill='x')

        self.table = customtkinter.CTkScrollableFrame(self)
        self.table.pack(padx=[5,5], pady=[5,5], fill='both', expand=True)

        self._rows = []

    def add_row(self) -> None:
        self._rows.append(Variable_row(self.table))
        self._rows[-1].grid(row=len(self._rows), column=0, padx=[0,0], pady=[0,0])
        return None
     
    def get_data(self) -> dict:
        self._data = {}
        for elem in self._rows:
            self._data[elem.name_entry.get()] = [float(elem.value_entry.get()), float(elem.error_entry.get())]
        return self._data

class Variable_row(customtkinter.CTkFrame):
    
    def __init__(self, master,
                 height: Union[int, float]=40,
                 width: Union[int, float]=400,
                 corner_radius: Union[int, float]=5):
        super().__init__(master, height=height, width=width, corner_radius=corner_radius)
    
        self.delete_button = customtkinter.CTkButton(self, height=25, width=25,
                                                      text='X',
                                                      command=lambda:self.delete_self(master))
        self.delete_button.pack(padx=[0, 0], pady=[2.5, 2.5], side='left')

        self.name_entry = customtkinter.CTkEntry(self, height=25, width=75, 
                                                 placeholder_text="Название")
        self.name_entry.pack(padx=[2.5, 0], pady=[2.5, 2.5], side='left')

        self.value_entry = customtkinter.CTkEntry(self, height=25, width=75, 
                                                 placeholder_text="Значение")
        self.value_entry.pack(padx=[2.5, 0], pady=[2.5, 2.5], side='left')

        self.error_entry = customtkinter.CTkEntry(self, height=25, width=100, 
                                                 placeholder_text="Погрешность")
        self.error_entry.pack(padx=[2.5, 0], pady=[2.5, 2.5], side='left')

    def delete_self(self, master) -> None:
        master.master.master.master._rows.remove(self)
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()