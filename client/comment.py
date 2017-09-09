import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from data_config import dc
from data_config import ad
from network import con


class Comment(tk.Frame):
    def __init__(self, tkControler, data):
        tk.Frame.__init__(self, master=tkControler)
        self.pack(fill=tk.BOTH, expand=True)
        self.__data = {}

        self.text = ""
        self.applicant = ""
        self.created_datetime = ""
        self.delate_id = ""
        self.id = ""
        self._modify_time = ""

        self.e_text = ScrolledText(master=self)

        self.data(data)
        self.widgets()
        # todo Buttony : add comment , obok każdego button edytuj comment
        # todo jeżeli masz admina lub jezeli jestes jego autorem..

    @property
    def modify_time(self):
        return self._modify_time

    @modify_time.setter
    def modify_time(self, value):
        if value is not None and value.lower() != "Null".lower():
            self._modify_time = value
        else:
            self._modify_time = ""


    def data(self, value):
        """
        Unpack data to class attributes
        :param value: Dictionary that contains payload from Serwer.
        :return:
        """
        self.text = value.get(dc.COMMENT, "")
        self.applicant = value.get(dc.APPLICANT, "")
        self.created_datetime = value.get(dc.CREATED_DT, "")
        self.delate_id = value.get(dc.DELATE_ID, "")
        self.id = value.get(dc.ID, "")
        self.modify_time = value.get(dc.MODIFY_TIME, "")
        self.__data = value

    def widgets(self):
        self.e_text.grid(row=1, column=0, columnspan=4)
        self.e_text.insert("1.0", self.text)
        if self.id != "0":
            self.e_text.configure(state=tk.DISABLED, height=5, width=80)
        else:
            self.e_text.configure(state=tk.NORMAL, height=5, width=50)
        # todo edit makeover
        # if self.saved is False:
        #     zapisz = tk.Button(self, text="zapisz", command=self.zapisz)
        #     zapisz.grid(row=0, column=3)

        l_ct = tk.Label(self, text="Utworzono\n{}".format(self.created_datetime))
        l_ct.grid(row=0, column=0)

        l_aplicant = tk.Label(self, text="Autor\n{}".format(ad.user_name(str(self.applicant))))
        l_aplicant.grid(row=0, column=1)

        l_mt = tk.Label(self, text="Modyfikowany\n{}".format(self.modify_time))
        l_mt.grid(row=0, column=2)

    def zapisz(self):
        self.__data[dc.COMMENT] = self.e_text.get("1.0", 'end-1c')

        response = con.post_comment(self.__data)

        if len(response) == 0:
            return 0
        # todo pobierz zwrócone dane i dodaj do komentarzy.
