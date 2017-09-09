# tk
import tkinter as tk
from tkinter import ttk

from user import user
from settings_window import Settings


class MenuCmd:
    def __init__(self, tkController):
        self.tkController = tkController

    # todo move to MainWindow
    def client_exit(self):
        self.tkController.quit()
        self.tkController.destroy()
        exit()

    @staticmethod
    def not_implemented():
        print("not implemented")

    def popupmsg(self, msg):
        popup = tk.Toplevel()
        popup.wm_title("Info")
        # popup.geometry("240x180")
        label = ttk.Label(popup, text=msg, justify=tk.CENTER)
        label.pack(pady=20, padx=20)
        B1 = ttk.Button(popup, text="ok", command=popup.destroy)
        B1.pack(side=tk.BOTTOM, pady=20)
        popup.mainloop()

    def info(self):
        self.popupmsg("MSR BugSors\nMichał Robaszewski\n2017")

    def save(self):
        tab_id = self.tkController.notebook.select()
        self.tkController.gallery[tab_id].zapisz()

    def settings(self):
        Settings(self.tkController)

    def add_delate(self):
        # TODO ten warunek do klasy user na is logged in true false
        # if user.user.login == "" or user.user.password == "" or user.user.token == "":
        if user.is_logged_in():
            Settings(self.tkController)
        else:
            # todo duplicated from nav_panel
            self.tkController.new_tab("*New", 0)

