# tk
import tkinter as tk
from tkinter import ttk

from user import user
from settings_window import Settings


class MenuCmd:
    """
    Manager class to proxy commands from Main Menu.
    """
    def __init__(self, tkController):
        self.main_window = tkController

    # todo move to MainWindow
    def client_exit(self):
        self.main_window.quit()
        self.main_window.destroy()
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
        tab_id = self.main_window.notebook.select()
        self.main_window.tab_gallery[tab_id].save_case_body()

    def settings(self):
        Settings(self.main_window)

    def add_case(self):
        """

        :return:
        """
        if not user.is_logged_in():
            Settings(self.main_window)
        else:
            # todo duplicated from nav_panel
            self.main_window.new_tab("*New", 0)

