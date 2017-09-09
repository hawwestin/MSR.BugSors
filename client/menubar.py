from tkinter import *
from menu_command import MenuCmd


class MainMenu:
    def __init__(self, tkController):
        """
        Menu controller.
        :param tkController: Tk from Main Window.
        """
        # Frame.__init__(self, parentFrame)
        self.tkController = tkController
        # Menu controller
        self.menu = Menu(self.tkController)
        self.tkController.config(menu=self.menu)

        self.menucmd = MenuCmd(self.tkController)
        self.menu_bar()

    def menu_bar(self):
        # creating a menu instance
        # open = Menu(self.menu, tearoff=0)
        # open.add_command(label="Login")
        # open.add_command(label="change connection", command=self.menucmd.settings)

        file = Menu(self.menu, tearoff=0)

        file.add_command(label="New", command=self.menucmd.add_delate)
        # file.add_cascade(label="Open connection", menu=open)
        file.add_command(label="Open connection", command=self.menucmd.settings)
        file.add_command(label="Reload")
        file.add_separator()
        file.add_command(label="Exit", command=self.menucmd.client_exit)
        self.menu.add_cascade(label="File", menu=file)

        edit = Menu(self.menu, tearoff=0)
        edit.add_command(label="Close Current Tab", command=self.tkController.close_Current_tab)
        self.menu.add_cascade(label="Edit", menu=edit)

        # view = Menu(self.menu, tearoff=0)
        # view.add_command(label="Full screen")
        # self.menu.add_cascade(label="View", menu=view)

        help = Menu(self.menu, tearoff=0)
        help.add_command(label="Info", command=self.menucmd.info)
        self.menu.add_cascade(label="Help", menu=help)

        self.tkController.config(menu=self.menu)
