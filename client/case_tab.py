import datetime
import tkinter as tk
from tkinter import ttk

from client.case_body import CaseInstance
from client.case import case_collection
from client.connection_module import com_switch
from client.data_config import StepData
from client.data_config import dict_accounts
from client.data_config import dict_account_type
from client.data_config import dict_case_status
from client.data_config import dict_priority
from client.step_body import StepBody
from client.step_instance import StepInstance
from client.tk_scrolled_frame import VerticalScrolledFrame as ScrolledFrame
from client.user import user
from client.steps import Steps


class CaseTab:
    """
    Notebook tab tkinter body that holds all widgets and aggregate data.
    """
    _padx = 8
    _pady = 3

    def __init__(self, main_window, parentFrame, case_instance: CaseInstance):
        self.main_window = main_window
        self.parent_frame = parentFrame
        self.data = case_instance

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
            self.com_frame_outline = tk.LabelFrame(self.containerBody, text="Steps")
            self.com_frame = ScrolledFrame(self.com_frame_outline)
            self.com_frame.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)
            self.containerBody.add(self.com_frame_outline, sticky='nse')

        self.lId = tk.Label(self.entry_space)
        self.lApplicant = tk.Label(self.entry_space)
        self.lCreate_time = tk.Label(self.entry_space)
        self.lModify_time = tk.Label(self.entry_space)
        self.lModify_by = tk.Label(self.entry_space)

        self.cbPriori = ttk.Combobox(self.entry_space)
        self.cbStatus = ttk.Combobox(self.entry_space)

        self.eName = tk.Entry(self.entry_space)
        self.tDescription = tk.Text(self.entry_space)
        self.tObjective = tk.Text(self.entry_space)
        self.tExpected = tk.Text(self.entry_space)
        self.tPost = tk.Text(self.entry_space)

        self.bUpdate = ttk.Button(self.but_line,
                                  text="Aktualizuj",
                                  command=self.update)
        self.bSave = ttk.Button(self.but_line,
                                text="Zapisz",
                                command=self.save_case_body)

        if int(self.data.id) > 0:
            self.dic_steps_gallery = {}
            self.case_steps = Steps()
            self.display_steps()

        # self.update_comment = False

        self.buttons()
        try:
            self.labels()
        except Exception as e:
            print(e)
            raise
        try:
            self.comboboxes()
        except Exception as e:
            print(e)
            raise
        try:
            self.entries()
        except Exception as e:
            print(e)
            raise

        # New case_instance has id =0 -> explicit False
        self.control(case_instance.id)

    @property
    def button_column(self):
        """
        Column iterator to align buttons.
        :return: next free column
        """
        self.__column += 1
        return self.__column

    @button_column.setter
    def button_column(self, value):
        if value < 0:
            self.__column = 0
        else:
            self.__column = 0

    def buttons(self):
        """
        Aggregate buttons inside tab.
        :return:
        """
        if int(self.data.id) > 0:
            self.bUpdate.grid(row=0, column=self.button_column, sticky='nsw')
        else:
            self.bSave.grid(row=0, column=self.button_column, sticky='nsw')

        if int(self.data.id) > 0:
            bEdit = ttk.Button(self.but_line, text="Edytuj",
                               command=self.edit_control)
            bEdit.grid(row=0, column=self.button_column, sticky='nsw')

        bCancel = ttk.Button(self.but_line, text="Cofnij",
                             command=self.undo)
        bCancel.grid(row=0, column=self.button_column, sticky='nsw')

        # if int(self.data.id) > 0:
        #     bKomentuj = ttk.Button(self.but_line, text="Skomentuj",
        #                            command=self.add_step_popup)
        #     bKomentuj.grid(row=0, column=self.button_column, sticky='nsw')

        bClose = ttk.Button(self.but_line, text="Zamknij", command=self.main_window.close_current_tab)
        bClose.grid(row=0, column=self.button_column, sticky='nse')

    def labels(self):
        """
        Aggregate static data to display on UI.
        With some drop dawns.
        :return:
        """
        labelRow = 0
        self.lId = ttk.Label(self.entry_space,
                             text="Id\n{}".format(self.data.id),
                             justify=tk.CENTER)
        self.lId.grid(row=labelRow,
                      column=0,
                      padx=CaseTab._padx)

        self.lCreate_time = ttk.Label(self.entry_space,
                                      text="Stworzono\n{}".format(str(self.data.create_time)),
                                      justify=tk.CENTER)
        self.lCreate_time.grid(row=labelRow,
                               column=1,
                               padx=CaseTab._padx)

        self.lApplicant = ttk.Label(self.entry_space,
                                    text="Twórca\n{}".format(dict_accounts.get_name(str(self.data.applicant))),
                                    justify=tk.CENTER)
        self.lApplicant.grid(row=labelRow,
                             column=2,
                             padx=CaseTab._padx)

        self.lModify_time = ttk.Label(self.entry_space,
                                      text="Zmodyfikowano\n{}".format(str(self.data.modify_time)),
                                      justify=tk.CENTER)
        self.lModify_time.grid(row=labelRow,
                               column=3,
                               padx=CaseTab._padx)

        self.lModify_by = ttk.Label(self.entry_space,
                                    text="Modifikowany przez\n{}".format(
                                        dict_accounts.get_name(str(self.data.modify_by))),
                                    justify=tk.CENTER)
        self.lModify_by.grid(row=labelRow,
                             column=4,
                             padx=CaseTab._padx)

    def comboboxes(self):
        l_priority = tk.Label(self.entry_space, text="Priority :")
        l_priority.grid(row=1,
                        column=0,
                        padx=CaseTab._padx,
                        pady=CaseTab._pady)

        # if str(self.data.status) == str(dict_case_status.close_status) or user.user_type == dict_account_type.admin:
        self.cbPriori.configure(value=dict_priority.names)

        self.cbPriori.set(dict_priority.get_name(self.data.priority))
        self.cbPriori.grid(row=1,
                           column=1,
                           padx=CaseTab._padx,
                           pady=CaseTab._pady)

        l_assigned = tk.Label(self.entry_space, text="Status :")
        l_assigned.grid(row=1,
                        column=2,
                        padx=CaseTab._padx,
                        pady=CaseTab._pady)

        self.cbStatus.configure(value=dict_case_status.names)
        self.cbStatus.set(dict_case_status.get_name(self.data.status))
        self.cbStatus.grid(row=1,
                           column=3,
                           padx=CaseTab._padx,
                           pady=CaseTab._pady)

    def entries(self):
        self.eName = tk.Text(self.entry_space,
                             wrap=tk.WORD,
                             height=2)
        self.eName.grid(row=2,
                        column=0,
                        columnspan=5,
                        pady=CaseTab._pady,
                        sticky='wn')
        self.eName.insert('1.0', self.data.name)

        self.tDescription = tk.Text(self.entry_space,
                                    wrap=tk.WORD)
        # self.tDescription.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.tDescription.insert('1.0', self.data.description)
        self.tDescription.grid(row=3,
                               column=0,
                               columnspan=5,
                               pady=CaseTab._pady,
                               sticky='wn')

        self.tObjective.configure(wrap=tk.WORD, height=8)
        self.tObjective.grid(row=4,
                             column=0,
                             columnspan=5,
                             pady=CaseTab._pady,
                             sticky='wn')
        self.tObjective.insert('1.0', self.data.objective)

        self.tExpected.configure(wrap=tk.WORD, height=5)
        self.tExpected.grid(row=5,
                            column=0,
                            columnspan=5,
                            pady=CaseTab._pady,
                            sticky='wn')
        self.tExpected.insert('1.0', self.data.expected_result)

        self.tPost.configure(wrap=tk.WORD, height=5)
        self.tPost.grid(row=6,
                        column=0,
                        columnspan=5,
                        pady=CaseTab._pady,
                        sticky='wn')
        self.tPost.insert('1.0', self.data.post_condition)

    def display_steps(self):
        """
        Reset current added steps and fetch from current connection new list.
        :return:
        """
        self.com_frame.destroy()
        self.com_frame = ScrolledFrame(self.com_frame_outline)
        self.com_frame.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)

        steps_order = com_switch.connection.get_steps(self.data.id)
        items = self.case_steps.sort_case_steps(steps_order)

        if len(items) == 0:
            # todo statusbar
            return
        for idx, data_step in enumerate(items):
            frame = tk.LabelFrame(self.com_frame.interior)
            frame.pack(fill=tk.BOTH, expand=True, anchor='nw')
            self.dic_steps_gallery[idx] = StepInstance(frame, data_step)

    def add_step_popup(self, name=""):
        """
        Display new window with entries to add new step.
        :param name:
        :return:
        """
        default_msg = "Nowy krok"
        if name == "":
            text = default_msg
        else:
            text = name

        def save():
            # if name != "":  # porównanie czy jest to Updatowy komentarz. jak będzie więcej porównać z listą .
            #     description = "{}\n{}".format(name, e_text.get("1.0", 'end-1c'))
            #     self.update_comment = True
            # else:
            description = e_text.get("1.0", 'end-1c')

            if self.save_step(description) == 1:
                self.update()
            popup.destroy()

        popup = tk.Toplevel()
        popup.wm_title("Dodaj krok")
        # popup.geometry("240x180")
        label = ttk.Label(popup, text=text, justify=tk.CENTER)
        label.pack(pady=20, padx=20)

        e_text = tk.Text(master=popup)
        e_text.pack(expand=True, fill=tk.BOTH)

        ok_button = ttk.Button(popup, text="ok", command=save)
        ok_button.pack(side=tk.BOTTOM, pady=20)

        popup.mainloop()

    def save_step(self, text):
        """
        Send new step via current connection.
        :return:
        """
        step = {StepData.NAME: "some fioeld data ",
                StepData.DESCRIPTION: text,
                StepData.ASSEMBLY: 1,  # data from dict .
                StepData.TYPE: 1,  # data from dict .
                StepData.APPLICANT: user.user_id,
                StepData.IS_ACTIVE: True,
                }

        response = com_switch.connection.post_step(StepBody(step))
        # todo bind it in current case if position was given

        if len(response) == 0:
            return 0
        else:
            self.display_steps()
            return 1

    def control(self, disable=True):
        """
        Switch control over ability to edit displayed data.
        :param disable:
        :return:
        """
        if disable:
            cb_state = state = tk.DISABLED
        else:
            state = tk.NORMAL
            cb_state = "readonly"
        self.tDescription.configure(state=state)
        self.eName.configure(state=state)
        self.tObjective.configure(state=state)
        self.tExpected.configure(state=state)
        self.tPost.configure(state=state)
        self.cbPriori.configure(state=cb_state)
        self.cbStatus.configure(state=cb_state)
        self.bUpdate.configure(state=state)

    def destroy(self):
        """
        Destroy current notebook tab.
        :return:
        """
        # todo inform window.notebook about it ?
        self.parent_frame.destroy()

    def save_case_body(self):
        """
        odsyła na serwer wprowadzone dane w pola , jeżeli odesłano z sukcesem zamyka karte i dodaje do listy
        :return:
        """
        self.data.description = self.tDescription.get("1.0", 'end-1c')
        self.data.name = self.eName.get("1.0", 'end-1c')
        self.data.status = dict_case_status.index(self.cbPriori.get())

        if case_collection.send_new_delate(self.data):
            self.main_window.navigator.populate_delate_list()
            self.destroy()
        else:
            # todo log status bar ... error handling.
            return None

    def edit_control(self):
        self.control(disable=False)

    def update(self):
        """
        zbierz dane z inputów i przeslij do serwera.
        :return:
        """
        # if str(self.data.status) != str(dict_case_status.index(self.cbPriori.get())):
        #     if self.update_comment:
        #         self.update_comment = False
        #     else:
        #         self.add_step_popup(
        #             "Zmiana statusu {} -> {}".format(dict_case_status.get_name(self.data.status), self.cbPriori.get()))
        #         return

        self.data.description = self.tDescription.get("1.0", 'end-1c')
        self.data.objective = self.tObjective.get("1.0", 'end-1c')
        self.data.expected_result = self.tExpected.get("1.0", 'end-1c')
        self.data.post_condition = self.tPost.get("1.0", 'end-1c')

        name_change = (self.data.name != self.eName.get("1.0", 'end-1c'))
        if name_change:
            self.data.name = self.eName.get("1.0", 'end-1c')
        self.data.priority = dict_priority.index(self.cbPriori.get())
        self.data.status = dict_case_status.index(self.cbStatus.get())

        if case_collection.save_case(self.data):
            self.main_window.navigator.populate_delate_list()
            if name_change:
                self.main_window.rename_tab(self.main_window.navigator.format_name(self.data.id, self.data.name),
                                            tab_body=self)
            self.data = case_collection.delateDict.get(int(self.data.id))
            self.undo()

    def format_name(self, idx, name):
        """
        Format tab name.
        :param idx:
        :param name:
        :return:
        """
        return "{:<5} {:<15}".format(idx, name)

    def undo(self):
        """
        Put again data from CaseInstance in data.
        :return:
        """
        self.control(False)

        self.eName.delete("1.0", tk.END)
        self.tDescription.delete("1.0", tk.END)
        self.tObjective.delete('1.0', tk.END)
        self.tExpected.delete('1.0', tk.END)
        self.tPost.delete('1.0', tk.END)

        self.eName.insert('1.0', self.data.name)
        self.tDescription.insert('1.0', self.data.description)
        self.tObjective.insert('1.0', self.data.objective)
        self.tExpected.insert('1.0', self.data.expected_result)
        self.tPost.insert('1.0', self.data.post_condition)

        self.cbStatus.set(dict_case_status.get_name(self.data.status))
        self.cbPriori.set(dict_priority.get_name(self.data.priority))
        self.lModify_time.configure(text="Zmodyfikowano\n{}".format(str(self.data.modify_time)))
        self.lModify_by.configure(
            text="Modifikowany przez\n{}".format(dict_accounts.get_name(str(self.data.modify_by))))

        if self.data.id != 0:
            self.control(True)
