# coding=utf-8
import json
from delate import delates
import delate_tab
import tkinter as tk
from menubar import *
from tkinter import ttk
from nav_panel import NavPanel
import utils


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        """
        Self its TK and Controler -> parent is a Frame
        :param args:
        :param kwargs:
        """
        # reference to the master widget, which is the tk window
        tk.Tk.__init__(self, *args, **kwargs)
        # self.Stylish()

        # self.configure(background='grey')

        # Try Panned window
        self.containerBody = tk.PanedWindow(self,
                                            sashwidth=6,
                                            showhandle=True,
                                            sashrelief=tk.RIDGE)
        self.containerBody.pack(fill=tk.BOTH, expand=True)
        # containerBody.configure(background='grey')

        self.title("BugSors")
        MainMenu(self)
        self.statusbar()

        self.navigator = NavPanel(self, self.containerBody)
        self.containerBody.add(self.navigator, sticky='wns')

        self.containerRight = tk.Frame(master=self.containerBody)
        self.containerBody.add(self.containerRight, sticky='nsew')

        self.notebook = ttk.Notebook(self.containerRight)
        self.notebook.pack(side="top", fill="both", expand=True)
        self.notebook.enable_traversal()
        self.gallery = {}

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

    # todo move tab logic to new module
    def new_tab(self, name, del_id):
        for tab_id in self.notebook.tabs():
            tab_name = self.notebook.tab(tab_id, "text")
            if self.gallery.get(tab_name, -1) != -1 and tab_name == name:
                self.notebook.select(tab_id)
                if name == "*New": #todo check if is valid
                    self.gallery[name].data = delates.create_delate_localy()
                return

        frame = ttk.Frame(self.notebook)
        frame.pack(fill=BOTH, expand=1)
        # todo dodawany jest podwójnie raz jako id 0 na liscie a raz pod id pobranym z serwera.
        if del_id > 0:
            if delates.delateDict.get(del_id, 0) != 0:
                self.gallery[name] = delate_tab.DelateTab(self, frame, delates.delateDict.get(del_id))
            else:
                print(json.dumps(delates.delateDict))

        else:
            self.gallery[name] = delate_tab.DelateTab(self, frame, delates.create_delate_localy())
        self.notebook.add(frame, text=name)
        self.notebook.select(self.notebook.index(tk.END)-1)

        # print(self.notebook.winfo_children())
        return frame

    def rename_tab(self, name, delate_tab):
        tab = self.notebook.index("current")
        self.notebook.tab(tab, text=name)
        self.gallery[name] = delate_tab

    def statusbar(self):
        utils.statusbar = Label(self, text=utils.statusmsg, bd=1, relief=SUNKEN, anchor=W)
        utils.statusbar.pack(side=BOTTOM, fill=X)

    def close_Current_tab(self):
        id = self.notebook.select()
        del_id = self.notebook.tab(id, "text")
        self.notebook.forget("current")
        # todo to zamyka tylko kartę potrzeba sksaować również obiekt by zwolnic pamiec
        self.gallery[del_id].destroy()
        self.gallery.pop(del_id)
