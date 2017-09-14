import tkinter as tk
from tkinter import font
from tkinter import ttk

from data_config import CaseData
from data_config import StepData
from utils import populate_constants
from case import case_collection
from settings_window import Settings
from user import user

DC = CaseData()
DCOM = StepData()


class NavPanel(tk.Frame):
    def __init__(self, main_window, parent_frame):
        """

            dList
            dList_gallery   słownik którego kluczem jest tekst wyświetlany
                            na liście wpisów w panelu nawigacyjnym, wartość
                            jest to ID zapisanego pod daną pozycją Delate.
        :param main_window:
        :param parent_frame:
        """
        tk.Frame.__init__(self, master=parent_frame)
        self.main_window = main_window

        self.menurow = tk.Frame(self)
        self.menurow.pack(side=tk.TOP)

        self.list = tk.Frame(self)
        self.list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.dlist = None
        self.dList_gallery = {}

        self.__widgets()

    def __widgets(self):
        """
        Tk widgets inside navigation frame.
        :return:
        """
        B1 = ttk.Button(self.menurow, text="Połącz", command=self.main_window.menu_command.establish_connection)
        B1.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        # B2 = ttk.Button(self.menurow, text="szukaj")
        # B2.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        B3 = ttk.Button(self.menurow, text="Dodaj", command=self.main_window.menu_command.add_case)
        B3.grid(row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)

        # preniesc font do Main window. lub innego pliku.
        list_font = font.Font(family='consolas', size=12, weight='normal')
        self.dlist = tk.Listbox(self.list, activestyle='underline',
                                bg='WHITE',
                                # height=15,
                                font=list_font)
        self.dlist.pack(expand=True, fill=tk.BOTH)
        self.dlist.bind("<Double-Button-1>", func=self.open_case)

    def populate_delate_list(self):
        """
        populate listbox with Case instances id and short name
        :return: None
        """
        self.dlist.delete(0, tk.END)
        # todo remake formatting in customizable panned table .
        self.dlist.insert(tk.END, "{:<5s} {:<15s}".format(DC.ID, DC.NAME))
        for row in sorted(case_collection.delateList):
            self.dlist.insert(tk.END, self.format_name(case_collection.delateDict[row].id,
                                                       case_collection.delateDict[row].name))
            # Zbudowanie slownika łączącego numer wiersza z wpisanym do niego Delate id
            self.dList_gallery[self.dlist.get(tk.END)] = case_collection.delateDict[row].id

    def format_name(self, idx, name):
        """
        Customizable formatting. with **kwargs and unpacking dict.
        Can by done after reformat of dList_gallery and open_case row_text variable.
        :param idx:
        :param name:
        :return:
        """
        return "{:<5} {:<15}".format(idx, name)

    def open_case(self, event):
        """
        Tk event handler for opening a selected row in dList.
        :param event:
        :return:
        """
        widget = event.widget
        selection = widget.curselection()
        row_text = widget.get(selection[0])
        del_id = int(self.dList_gallery.get(row_text, 0))
        # Row id 0 is reserved for column names and not represent any Case.
        if del_id != 0:
            self.main_window.new_tab(row_text, del_id)
