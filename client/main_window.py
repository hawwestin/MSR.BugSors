# coding=utf-8
import json
import tkinter as tk
from tkinter import ttk

import client.utils as utils
from client.case_tab import CaseTab
from client.case import case_collection
from client.menu_bar import *
from client.nav_panel import NavPanel
from client.connection_module import com_switch
from client.connection_module import Database
from client.menu_command import MenuCmd


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        """
        Main application class that aggregate other instances and windows.
        :param args:
        :param kwargs:
        """
        # reference to the master widget, which is the tk window
        tk.Tk.__init__(self, *args, **kwargs)
        # self.Stylish()

        self.containerBody = tk.PanedWindow(self,
                                            sashwidth=6,
                                            showhandle=True,
                                            sashrelief=tk.RIDGE)
        self.containerBody.pack(fill=tk.BOTH, expand=True)

        # switch of connection !
        com_switch.connection = Database(adres="../db/test_local.db")

        self.menu_command = MenuCmd(self)
        self.main_menu = MainMenu(self)

        utils.status_message = tk.StringVar()
        utils.status_message.set('')
        self.status_bar = tk.Label(self, textvariable=utils.status_message, bd=1, relief=tk.SUNKEN,
                                   anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.navigator = NavPanel(self, self.containerBody)
        self.containerBody.add(self.navigator, sticky='wns')

        self.containerRight = tk.Frame(master=self.containerBody)
        self.containerBody.add(self.containerRight, sticky='nsew')

        self.notebook = ttk.Notebook(self.containerRight)
        self.notebook.pack(side="top", fill="both", expand=True)
        self.notebook.enable_traversal()
        self.notebook.bind("<<NotebookTabChanged>>", func=self.diag)
        self.tab_gallery = {}

    def diag(self, event):
        # todo check other methods for changing tabs.
        print(event)
        # print(event.keys())

    def Stylish(self):
        _bgcolor = 'blue'  # RGV value #f5deb3
        _fgcolor = '#000000'  # Closest X11 color: 'black'
        _compcolor = '#b2c9f4'  # Closest X11 color: 'SlateGray2'
        _ana1color = '#eaf4b2'  # Closest X11 color: '{pale goldenrod}'
        _ana2color = '#f4bcb2'  # Closest X11 color: 'RosyBrown2'
        font10 = "-family {DejaVu Sans} -size 14 -weight normal -slant roman -underline 0 -overstrike 0"

        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font=font10)
        self.style.map('.', background=[('selected', _compcolor), ('active', _ana2color)])

        self.style.configure('TNotebook.Tab', background=_bgcolor)
        self.style.configure('TNotebook.Tab', foreground=_fgcolor)
        self.style.map('TNotebook.Tab', background=[('selected', _compcolor), ('active', _ana2color)])

    def new_tab(self, name, del_id):
        """
        Check if tab is already open if is open switch to it.
        If not open yet create new frame and append it to notebook with new tab object.

        If tab_id == 0  indicate to create brand new object locally and append it to lists and dicts
        :param name: tab name from self.notebook
        :param del_id:
        :return:
        """
        for tab_id in self.notebook.tabs():
            tab_name = self.notebook.tab(tab_id, "text")
            if self.tab_gallery.get(tab_name, -1) != -1 and tab_name == name:
                self.notebook.select(tab_id)
                if name == "*New":  # todo check if is valid
                    self.tab_gallery[name].data = case_collection.create_case_locally()
                return None

        frame = ttk.Frame(master=self.notebook, name=str(del_id))
        frame.pack(fill=BOTH, expand=1)
        # todo dodawany jest podwójnie raz jako id 0 na liscie a raz pod id pobranym z serwera.
        if del_id > 0:
            if case_collection.delateDict.get(del_id, 0) != 0:
                self.tab_gallery[name] = CaseTab(self, frame, case_collection.delateDict.get(del_id))
            else:
                print(json.dumps(case_collection.delateDict))

        else:
            self.tab_gallery[name] = CaseTab(self, frame, case_collection.create_case_locally())
        self.notebook.add(frame, text=name)
        self.notebook.select(self.notebook.index(tk.END) - 1)

        # print(self.notebook.winfo_children())
        return frame

    def rename_tab(self, name, tab_body: "CaseTab"):
        """
        Change tab name for current selected tab.
        :param name:
        :param tab_body:
        :return:
        """
        tab = self.notebook.index("current")
        self.notebook.tab(tab, text=name)
        # todo drop old name from tab_gallery ?
        self.tab_gallery[name] = tab_body

    def close_current_tab(self):
        """
        Call delate on case_tab instance and pop it from tab_gallery.
        :return:
        """
        id = self.notebook.select()
        del_id = self.notebook.tab(id, "text")
        self.notebook.forget("current")
        # todo to zamyka tylko kartę potrzeba sksaować również obiekt by zwolnic pamiec
        self.tab_gallery[del_id].destroy()
        self.tab_gallery.pop(del_id)
