from data_config import CaseData


class CaseInstance:
    def __init__(self, value: dict):
        # todo remake to kwargs

        self.id = None
        self.name = None
        self.description = None
        self.status = None
        self.priority = None
        self.objective = None
        self.expected_result = None
        self.post_condition = None

        self.applicant = None
        self.create_time = None
        self._modify_time = ""
        self.modify_time = None
        self._modify_by = ""
        self.modify_by = None
        self.is_active = None

        self.data = value
        self.update(value)
        """
        Key - Step ID , value previous step id. to create chain. 
        """
        self.dictComments = {}

        # value is a tuple of step _id and previous_step_id.
        self.step_chain = []

    def update(self, value):
        self.id = value.get(CaseData.ID, self.id)
        self.name = value.get(CaseData.NAME, self.name)
        self.description = value.get(CaseData.DESCRIPTION, self.description)
        self.applicant = value.get(CaseData.APPLICANT, self.applicant)
        self.create_time = value.get(CaseData.CREATE_TIME, self.create_time)
        self.status = value.get(CaseData.STATUS, self.status)
        self._modify_time = ""
        self.modify_time = value.get(CaseData.MODIFY_TIME, self.modify_time)
        self._modify_by = ""
        self.modify_by = value.get(CaseData.MODIFY_BY, self.modify_by)
        self.is_active = value.get(CaseData.IS_ACTIVE, self.is_active)

        self.data = value

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

    def post_data(self):
        """
        provide formated string to insert to db
        :return:
        """
        return ", ".join(["'{}'".format(self.data.get(str(value), "null")) for value in CaseData.post])


if __name__ == '__main__':
    data = {}
    data[CaseData.ID] = '1'
    data[CaseData.NAME] = 'name'
    data[CaseData.DESCRIPTION] = 'desc'
    data[CaseData.STATUS] = '1'
    data[CaseData.PRIORITY] = '1'
    data[CaseData.OBJECTIVE] = 'obj'
    data[CaseData.EXPECTED_RESULT] = 'exp'
    data[CaseData.POST_CONDITION] = 'post cond'
    data[CaseData.APPLICANT] = '1'
    data[CaseData.IS_ACTIVE] = '1'

    case = CaseInstance(data)
    print(case.post_data())
