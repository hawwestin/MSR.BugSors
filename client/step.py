import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from data_config import StepData
from data_config import ad
from network import con
from step_body import StepBody

class Step(tk.Frame):
    def __init__(self, tkControler, data):
        tk.Frame.__init__(self, master=tkControler)
        self.pack(fill=tk.BOTH, expand=True)

        self.body = StepBody(data)

        self.e_text = ScrolledText(master=self)

        self.widgets()
        # todo Buttony : add comment , obok każdego button edytuj comment
        # todo jeżeli masz admina lub jezeli jestes jego autorem..

    def widgets(self):
        self.e_text.grid(row=1, column=0, columnspan=4)
        self.e_text.insert("1.0", self.body.name)
        if self.body.id != "0":
            self.e_text.configure(state=tk.DISABLED, height=5, width=80)
        else:
            self.e_text.configure(state=tk.NORMAL, height=5, width=50)
        # todo edit makeover
        # if self.saved is False:
        #     zapisz = tk.Button(self, text="zapisz", command=self.zapisz)
        #     zapisz.grid(row=0, column=3)

        l_ct = tk.Label(self, text="Utworzono\n{}".format(self.body.created_datetime))
        l_ct.grid(row=0, column=0)

        l_aplicant = tk.Label(self, text="Autor\n{}".format(ad.user_name(str(self.body.applicant))))
        l_aplicant.grid(row=0, column=1)

        l_mt = tk.Label(self, text="Modyfikowany\n{}".format(self.body.modify_time))
        l_mt.grid(row=0, column=2)

    def zapisz(self):
        self.body.data[StepData.NAME] = self.e_text.get("1.0", 'end-1c')

        response = con.post_step(self.body.data)

        if len(response) == 0:
            return 0
        # todo pobierz zwrócone dane i dodaj do komentarzy.
