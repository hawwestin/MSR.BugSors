import tkinter as tk

from connection_module import com_switch
from data_config import Accounts
from user import user
from utils import populate_constants


class Settings(tk.Toplevel):
    """
    Support window to configure application.
    """
    def __init__(self, tkController, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # todo check if its open and no open another.
        self.tkController = tkController

        self.labelCrud = tk.LabelFrame(self,
                                       text="Logowanie")
        self.labelCrud.pack(fill=tk.BOTH, expand=True)

        self.e_login = tk.Entry(self.labelCrud)
        self.e_password = tk.Entry(self.labelCrud, show='*')
        self.authenticate()

        self.labelCon = tk.LabelFrame(self,
                                      text="Adres serwera")
        self.labelCon.pack(fill=tk.BOTH, expand=True)
        # adres = Str
        self.e_adress = tk.Entry(self.labelCon)
        self.config()

        self.statusbar = tk.Label(self, text="", bd=1, relief=tk.SUNKEN, anchor='w')
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.mainloop()

    def config(self):
        l_adress = tk.Label(self.labelCon, text="Adres serwera")
        l_adress.grid(row=0, column=0)
        self.e_adress.grid(row=0, column=1)

        b_con = tk.Button(self.labelCon, text="zapisz", command=self.save_addr)
        b_con.grid()

    def authenticate(self):
        l_login = tk.Label(self.labelCrud, text="Login")
        l_login.grid(row=0, column=0)
        self.e_login.grid(row=0, column=1)

        l_pass = tk.Label(self.labelCrud, text="Hasło")
        l_pass.grid(row=1, column=0)
        self.e_password.grid(row=1, column=1)

        b_con = tk.Button(self.labelCrud, text="Zaloguj", command=self.login)
        b_con.grid()

    def save_addr(self):
        # todo sprawdanie poprawnosci wprowadzonego adresu
        if self.e_adress.get() != "":
            com_switch.connection.configure(self.e_adress.get())
            self.statusbar.configure(text="Zapisano adres")
        else:
            self.statusbar.configure(text="Wprowadz adres serwera")

    def login(self):
        if self.e_login.get() != "" and self.e_password.get() != "":
            if self.auth(login=self.e_login.get(), password=self.e_password.get()) == 1:
                self.statusbar.configure(text="zalogowano, możesz zamknąć okno ")
                populate_constants()
            else:
                self.statusbar.configure(text="Błędny login lub hasło")
        else:
            self.statusbar.configure(text="Wprowadź login i hasło")

    def auth(self, login, password):
        """
        puknij do serwera z loginem i hasłem i ustaw token
        :return:
        """
        # global connection
        user.login = login
        user.password = password

        response = com_switch.connection.login()
        if len(response) == 0:
            return 0
        if response.get(Accounts.TOKEN, 0) == 0 \
                or response.get(Accounts.Account_TYPE, 0) == 0 \
                or response.get(Accounts.ID) == 0:
            # Auth token is empty or sth else

            return 0
        user.token = response.get(Accounts.TOKEN, "")
        user.user_id = response.get(Accounts.ID, 0)
        user.user_type = response.get(Accounts.Account_TYPE, 0)

        return 1
