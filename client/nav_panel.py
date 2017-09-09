import tkinter as tk
from tkinter import font
from tkinter import ttk

from data_config import DelateData
from data_config import CommentData
from utils import populate_constants
from delate import delates
from settings_window import Settings
from user import user

DC = DelateData()
DCOM = CommentData()


class NavPanel(tk.Frame):
    def __init__(self, tkControler, parentFrame):
        """

            dList
            dList_gallery   słownik którego kluczem jest tekst wyświetlany
                            na liście wpisów w panelu nawigacyjnym, wartość
                            jest to ID zapisanego pod daną pozycją Delate.
        :param tkControler:
        :param parentFrame:
        """
        tk.Frame.__init__(self, master=parentFrame)
        self.tkController = tkControler

        self.menurow = tk.Frame(self)
        self.menurow.pack(side=tk.TOP)

        self.list = tk.Frame(self)
        self.list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.dlist = None
        self.dList_gallery = {}

        self.widgets()

    def widgets(self):
        B1 = ttk.Button(self.menurow, text="Połącz", command=self.connect)
        B1.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        # B2 = ttk.Button(self.menurow, text="szukaj")
        # B2.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
        B3 = ttk.Button(self.menurow, text="Dodaj", command=self.add_delate)
        B3.grid(row=0, column=2, sticky=tk.N + tk.S + tk.E + tk.W)

        # preniesc font do Main window. lub innego pliku.
        list_font = font.Font(family='consolas', size=12, weight='normal')
        self.dlist = tk.Listbox(self.list, activestyle='underline',
                                bg='WHITE',
                                # height=15,
                                font=list_font)
        self.dlist.pack(expand=True, fill=tk.BOTH)
        self.dlist.bind("<Double-Button-1>", func=self.open_delate)

    def connect(self):
        if user.login == "" or user.password == "":
            Settings(self.tkController)
        else:
            populate_constants()
            delates.get_delate()
            self.populate_delate_list()

    def populate_delate_list(self):
        self.dlist.delete(0, tk.END)
        self.dlist.insert(tk.END, "{:<5s} {:<15s}".format(DC.ID, DC.NAME))
        for row in sorted(delates.delateList):
            self.dlist.insert(tk.END, self.format_name(delates.delateDict[row].id,
                                                       delates.delateDict[row].name))
            # Zbudowanie slownika łączącego numer wiersza z wpisanym do niego Delate id
            self.dList_gallery[self.dlist.get(tk.END)] = delates.delateDict[row].id

    def format_name(self, idx, name):
        return "{:<5} {:<15}".format(idx, name)

    def open_delate(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        del_id = int(self.dList_gallery.get(value, 0))
        if del_id != 0:
            self.tkController.new_tab(value, del_id)

    def add_delate(self):
        if user.is_logged_in():
            Settings(self.tkController)
        else:
            # todo is duplicated to MenuCmd
            self.tkController.new_tab("*New", 0)
