import datetime
import tkinter as tk
from tkinter import ttk

from comment import Comment
from data_config import atDict
from data_config import dc
from data_config import ds
from data_config import ad
from delate import delates
from network import con
from user import user
from tk_scrolled_frame import VerticalScrolledFrame as ScrolledFrame


class DelateTab:
    def __init__(self, tkControler, parentFrame, delate):
        self.tkControler = tkControler
        self.parentframe = parentFrame
        self.data = delate

        self.delFrame = tk.Frame(parentFrame)
        self.delFrame.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)
        self.but_line = tk.Frame(self.delFrame, relief=tk.SUNKEN)
        self.but_line.pack(side=tk.TOP, anchor=tk.NW)
        self.__column = 0

        self.containerBody = tk.PanedWindow(self.delFrame,
                                            sashwidth=6,
                                            showhandle=True,
                                            sashrelief=tk.RIDGE,
                                            handlesize=11)
        self.containerBody.pack(fill=tk.BOTH, expand=True)

        self.entry_space = tk.Frame(self.containerBody)
        # self.entry_space.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.BOTH, expand=True)
        self.containerBody.add(self.entry_space, sticky='wns')

        if int(self.data.id) > 0:
            self.com_frame_outline = tk.LabelFrame(self.containerBody, text="Comments")
            self.com_frame = ScrolledFrame(self.com_frame_outline)
            self.com_frame.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)
            self.containerBody.add(self.com_frame_outline, sticky='nse')

        self.tDescription = tk.Text(self.entry_space)
        self.lId = tk.Label(self.entry_space)
        self.eName = tk.Entry(self.entry_space)
        self.lApplicant = tk.Label(self.entry_space)
        self.cbAssigned = ttk.Combobox(self.entry_space)
        self.cbStatus = ttk.Combobox(self.entry_space)
        self.lCreate_time = tk.Label(self.entry_space)
        self.lModify_time = tk.Label(self.entry_space)
        self.lModify_by = tk.Label(self.entry_space)

        self.bAktualizuj = ttk.Button(self.but_line,
                                      text="Aktualizuj",
                                      command=self.aktualizuj)
        self.bSave = ttk.Button(self.but_line,
                                text="Zapisz",
                                command=self.zapisz)

        if int(self.data.id) > 0:
            # self.new_comment = False
            self.dicComments_gallery = {}
            self.comments()

        self.update_comment = False

        self.buttons()
        self.entries()

        # New delate has id =0 -> explicit False
        self.control(delate.id)

    @property
    def button_column(self):
        self.__column += 1
        return self.__column

    @button_column.setter
    def button_column(self, value):
        if value < 0:
            self.__column = 0
        else:
            self.__column = 0

    def buttons(self):
        if int(self.data.id) > 0:
            self.bAktualizuj.grid(row=0, column=self.button_column, sticky='nsw')
        else:
            self.bSave.grid(row=0, column=self.button_column, sticky='nsw')

        if int(self.data.id) > 0:
            bEdit = ttk.Button(self.but_line, text="Edytuj",
                               command=self.edytuj)
            bEdit.grid(row=0, column=self.button_column, sticky='nsw')

        bCancel = ttk.Button(self.but_line, text="Cofnij",
                             command=self.cofnij)
        bCancel.grid(row=0, column=self.button_column, sticky='nsw')

        if int(self.data.id) > 0:
            bKomentuj = ttk.Button(self.but_line, text="Skomentuj",
                                   command=self.add_comment_popup)
            bKomentuj.grid(row=0, column=self.button_column, sticky='nsw')

        bClose = ttk.Button(self.but_line, text="Zamknij", command=self.tkControler.close_Current_tab)
        bClose.grid(row=0, column=self.button_column, sticky='nse')

    def entries(self):
        labelRow = 0
        _padx = 8
        _pady = 3
        # todo dorobic labelki koło pozycji do wpisywanai tekstu. lub w label framy.
        self.lId = ttk.Label(self.entry_space,
                             text="Id\n{}".format(self.data.id),
                             justify=tk.CENTER)
        self.lId.grid(row=labelRow,
                      column=0,
                      padx=_padx)

        self.lCreate_time = ttk.Label(self.entry_space,
                                      text="Stworzono\n{}".format(str(self.data.create_time)),
                                      justify=tk.CENTER)
        self.lCreate_time.grid(row=labelRow,
                               column=1,
                               padx=_padx)

        self.lApplicant = ttk.Label(self.entry_space,
                                    text="Zgłaszający\n{}".format(ad.user_name(str(self.data.applicant))),
                                    justify=tk.CENTER)
        self.lApplicant.grid(row=labelRow,
                             column=2,
                             padx=_padx)

        self.lModify_time = ttk.Label(self.entry_space,
                                      text="Zmodyfikowano\n{}".format(str(self.data.modify_time))
                                      , justify=tk.CENTER)
        self.lModify_time.grid(row=labelRow,
                               column=3,
                               padx=_padx)

        self.lModify_by = ttk.Label(self.entry_space,
                                    text="Modifikowany przez\n{}".format(ad.user_name(str(self.data.modify_by))),
                                    justify=tk.CENTER)
        self.lModify_by.grid(row=labelRow,
                             column=4,
                             padx=_padx)

        l_status = tk.Label(self.entry_space, text="Status :")
        l_status.grid(row=1,
                      column=0,
                      padx=_padx,
                      pady=_pady)

        if str(self.data.status) == str(ds.close_status) or user.user_type == atDict.admin:
            self.cbStatus.configure(value=ds.names)
        else:
            self.cbStatus.configure(value=ds.names_unclose)

        self.cbStatus.set(ds.state_name(self.data.status))
        self.cbStatus.grid(row=1,
                           column=1,
                           padx=_padx,
                           pady=_pady)

        l_assigned = tk.Label(self.entry_space, text="Przypisany :")
        l_assigned.grid(row=1,
                        column=3,
                        padx=_padx,
                        pady=_pady)

        self.cbAssigned.configure(value=ad.names)
        self.cbAssigned.set(ad.user_name(self.data.assigned))
        self.cbAssigned.grid(row=1,
                             column=4,
                             padx=_padx,
                             pady=_pady)

        self.eName = tk.Text(self.entry_space,
                             wrap=tk.WORD,
                             height=2)
        self.eName.grid(row=2,
                        column=0,
                        columnspan=5,
                        pady=_pady,
                        sticky='wn')
        self.eName.insert('1.0', self.data.name)

        self.tDescription = tk.Text(self.entry_space,
                                    wrap=tk.WORD)
        # self.tDescription.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.tDescription.insert('1.0', self.data.description)
        self.tDescription.grid(row=3,
                               column=0,
                               columnspan=5,
                               pady=_pady,
                               sticky='wn')

    def comments(self):
        # todo skasuj istniejące framy w label frame comments i wstaw ponownie.
        self.com_frame.destroy()
        self.com_frame = ScrolledFrame(self.com_frame_outline)
        self.com_frame.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)

        items = con.get_comments(self.data.id)

        if len(items) == 0:
            # todo statusbar
            return
        # todo order by id . by najstarsze byly nadole.
        for com in items:
            com_id = str(com.get(dc.ID, 0))
            if str(com.get(dc.IS_ACTIVE, 0)) == "1" and com_id is not 0:
                frame = tk.LabelFrame(self.com_frame.interior)
                frame.pack(fill=tk.BOTH, expand=True, anchor='nw')
                self.dicComments_gallery[com_id] = Comment(frame, com)

    def add_comment_popup(self, title=""):
        default_msg = "Nowy komentarz"
        if title == "":
            text = default_msg
        else:
            text = title

        def save():
            if title != "":  # porównanie czy jest to Updatowy komentarz. jak będzie więcej porównać z listą .
                com = "{}\n{}".format(title, e_text.get("1.0", 'end-1c'))
                self.update_comment = True
            else:
                com = e_text.get("1.0", 'end-1c')
            if self.add_comment(com) == 1:
                self.aktualizuj()
            popup.destroy()

        popup = tk.Toplevel()
        popup.wm_title("Dodaj komentarz")
        # popup.geometry("240x180")
        label = ttk.Label(popup, text=text, justify=tk.CENTER)
        label.pack(pady=20, padx=20)

        e_text = tk.Text(master=popup)
        e_text.pack(expand=True, fill=tk.BOTH)

        ok_button = ttk.Button(popup, text="ok", command=save)
        ok_button.pack(side=tk.BOTTOM, pady=20)

        popup.mainloop()

    def add_comment(self, text):
        """

        :return:
        """
        com = {dc.APPLICANT: user.user_id,
               dc.IS_ACTIVE: 1,
               dc.CREATED_DT: datetime.datetime.now(),
               dc.DELATE_ID: self.data.id,
               dc.COMMENT: text,
               dc.ID: "0",
               dc.MODIFY_TIME: ""
               }

        response = con.post_comment(com)

        if len(response) == 0:
            return 0
        else:
            self.comments()
            return 1

    def control(self, disable=True):
        if disable:
            cb_state = state = tk.DISABLED
        else:
            state = tk.NORMAL
            cb_state = "readonly"
        self.tDescription.configure(state=state)
        self.eName.configure(state=state)
        if user.user_type == atDict.admin:
            self.cbAssigned.configure(state=cb_state)
        else:
            self.cbAssigned.configure(state=tk.DISABLED)
        self.cbStatus.configure(state=cb_state)
        self.bAktualizuj.configure(state=state)

    def destroy(self):
        self.parentframe.destroy()

    def zapisz(self):
        """
        odsyła na serwer wprowadzone dane w pola , jeżeli odesłano z sukcesem zamyka karte i dodaje do listy
        :return:
        """
        self.data.description = self.tDescription.get("1.0", 'end-1c')
        self.data.name = self.eName.get("1.0", 'end-1c')
        self.data.status = ds.state_idx(self.cbStatus.get())
        if int(user.user_type) == int(atDict.admin):
            self.data.assigned = ad.user_idx(self.cbAssigned.get())

        if delates.send_new_delate(self.data):
            self.tkControler.navigator.populate_delate_list()
            self.destroy()

    def edytuj(self):
        self.control(disable=False)

    def aktualizuj(self):
        """
        zbierz dane z inputów i przeslij do serwera.
        :return:
        """
        if str(self.data.status) != str(ds.state_idx(self.cbStatus.get())):
            if self.update_comment:
                self.update_comment = False
            else:
                self.add_comment_popup(
                    "Zmiana statusu {} -> {}".format(ds.state_name(self.data.status), self.cbStatus.get()))
                return

        self.data.description = self.tDescription.get("1.0", 'end-1c')
        name_change = (self.data.name != self.eName.get("1.0", 'end-1c'))
        if name_change:
            self.data.name = self.eName.get("1.0", 'end-1c')
        self.data.assigned = ad.user_idx(self.cbAssigned.get())
        self.data.status = ds.state_idx(self.cbStatus.get())

        if delates.save_delate(self.data):
            self.tkControler.navigator.populate_delate_list()
            if name_change:
                self.tkControler.rename_tab(self.tkControler.navigator.format_name(self.data.id, self.data.name),
                                            delate_tab=self)
            self.data = delates.delateDict.get(int(self.data.id))
            self.cofnij()

    def cofnij(self):
        """
        wstaw w pola ponownie wartości z serwera.
        :return:
        """
        self.control(False)

        self.eName.delete("1.0", tk.END)
        self.tDescription.delete("1.0", tk.END)

        self.eName.insert('1.0', self.data.name)
        self.tDescription.insert('1.0', self.data.description)
        self.cbStatus.set(ds.state_name(self.data.status))
        self.lModify_time.configure(text="Zmodyfikowano\n{}".format(str(self.data.modify_time)))
        self.lModify_by.configure(text="Modifikowany przez\n{}".format(ad.user_name(str(self.data.modify_by))))

        if self.data.id != 0:
            self.control(True)
