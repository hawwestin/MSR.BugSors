from tkinter import *


class MainMenu:
    def __init__(self, main_window):
        """
        Main Menu controller.
        :param main_window: Tk from Main Window.
        """
        # Frame.__init__(self, parentFrame)
        self.main_window = main_window
        # Menu controller
        self.menu = Menu(self.main_window)
        self.main_window.config(menu=self.menu)

        self.menu_command = main_window.menu_command
        self.menu_bar()

    def menu_bar(self):
        # creating a menu instance
        # open = Menu(self.menu, tearoff=0)
        # open.add_command(label="Login")
        # open.add_command(label="change connection", command=self.menu_command.settings)

        file = Menu(self.menu, tearoff=0)

        file.add_command(label="New", command=self.menu_command.add_case)
        # file.add_cascade(label="Open connection", menu=open)
        file.add_command(label="Settings", command=self.menu_command.settings)
        file.add_command(label="Reload", command=self.menu_command.establish_connection)
        file.add_separator()
        file.add_command(label="Exit", command=self.menu_command.client_exit)
        self.menu.add_cascade(label="File", menu=file)

        edit = Menu(self.menu, tearoff=0)
        edit.add_command(label="Close Current Tab", command=self.main_window.close_current_tab)
        self.menu.add_cascade(label="Edit", menu=edit)

        # view = Menu(self.menu, tearoff=0)
        # view.add_command(label="Full screen")
        # self.menu.add_cascade(label="View", menu=view)

        help = Menu(self.menu, tearoff=0)
        help.add_command(label="Info", command=self.menu_command.info)
        self.menu.add_cascade(label="Help", menu=help)

        self.main_window.config(menu=self.menu)
