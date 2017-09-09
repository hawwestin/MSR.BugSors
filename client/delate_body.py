class DelateInstance:
    def __init__(self, id, name, desc, app, ass, stat, create, mtime, mby):
        self.id = id
        self.name = name
        self.description = desc
        self.applicant = app
        self.__assigned = ass
        self.status = stat
        self.create_time = create
        self._modify_time = ""
        self.modify_time = mtime

        self._modify_by = ""
        self.modify_by = mby

        self.aggregated = {}
        """
        Key Id . Value Data. mayby dict of Msg, author and date.
        """
        self.dictComments = {}

    @property
    def assigned(self):
        """
        zwrocenie nazwy nie idka konta.
        :return:
        """
        return self.__assigned

    @assigned.setter
    def assigned(self, value):
        """
        ze słownikowanie z słownika kont na idka tego konta.
        :param value:
        :return:
        """
        if value is not None and value.lower() != "Null".lower():
            self.__assigned = value
            pass
        else:
            self.__assigned = ""

    @property
    def modify_time(self):
        return self._modify_time

    @modify_time.setter
    def modify_time(self, value):
        if value is not None and value.lower() != "Null".lower():
            self._modify_time = value
        else:
            self._modify_time = " "

    @property
    def modify_by(self):
        return self._modify_by

    @modify_by.setter
    def modify_by(self, value):
        if value is not None and value.lower() != "Null".lower():
            self._modify_by = value
        else:
            self._modify_by = ""
