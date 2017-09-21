from client.user import user
from client.data_config import CaseData
from client.data_config import dict_accounts


# todo rename na body
class CaseInstance:
    def __init__(self, **kwargs):
        # todo remake to kwargs

        self.id = None
        self._name = None
        self._description = ""
        self._status = ""
        self._priority = ""
        self._objective = ""
        self._expected_result = ""
        self._post_condition = ""

        self.applicant = None
        self.create_time = None
        self._modify_time = ""
        self.modify_time = None
        self._modify_by = ""
        self.modify_by = None
        self.is_active = None

        self.data = dict(kwargs)
        self.update(**kwargs)
        """
        Key - StepInstance ID , value previous step id. to create chain. 
        """
        self.dictComments = {}

        # value is a tuple of step _id and previous_step_id.
        self.step_chain = []

    def update(self, **value):
        self.id = value.get(CaseData.ID, self.id)
        self.name = value.get(CaseData.NAME, self.name)
        self.description = value.get(CaseData.DESCRIPTION, self.description)
        self.status = value.get(CaseData.STATUS, self.status)
        self.priority = value.get(CaseData.PRIORITY, self.priority)
        self.objective = value.get(CaseData.OBJECTIVE, self.objective)
        self.expected_result = value.get(CaseData.EXPECTED_RESULT, self.expected_result)
        self.post_condition = value.get(CaseData.POST_CONDITION, self.post_condition)

        self.applicant = value.get(CaseData.APPLICANT, self.applicant)
        self.create_time = value.get(CaseData.CREATE_TIME, self.create_time)
        self.modify_time = value.get(CaseData.MODIFY_TIME, self.modify_time)
        self.modify_by = value.get(CaseData.MODIFY_BY, self.modify_by)
        self.is_active = value.get(CaseData.IS_ACTIVE, self.is_active)

        self.data.update(value)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value
        self.data.update({CaseData.DESCRIPTION: self._description})

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.data.update({CaseData.NAME: self._name})

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        # todo check if its an ID
        self._status = value
        self.data.update({CaseData.STATUS: self._status})

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        # todo check if its an ID
        self._priority = value
        self.data.update({CaseData.PRIORITY: self._priority})

    @property
    def objective(self):
        return self._objective

    @objective.setter
    def objective(self, value):
        self._objective = value
        self.data.update({CaseData.OBJECTIVE: self._objective})

    @property
    def expected_result(self):
        return self._expected_result

    @expected_result.setter
    def expected_result(self, value):
        self._expected_result = value
        self.data.update({CaseData.EXPECTED_RESULT: self._expected_result})

    @property
    def post_condition(self):
        return self._post_condition

    @post_condition.setter
    def post_condition(self, value):
        self._post_condition = value
        self.data.update({CaseData.POST_CONDITION: self._post_condition})

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
        if value is not None and str(value).lower() != "Null".lower():
            self._modify_by = value
            self.data.update({CaseData.MODIFY_BY: dict_accounts.index(self._modify_by)})
        else:
            self._modify_by = ""

    def put_data(self):
        """
        formatted string to update record in database.
        :return:STRING list of pairs column name = '{value}' , ...
        """
        self.modify_by = user.login
        return ", ".join(["{} = '{}'".format(value, self.data.get(str(value), "null")) for value in CaseData.put])

    def post_data(self):
        """
        provide formated string to insert to db
        :return:
        """
        self.applicant = user.login
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

    case = CaseInstance(**data)
    print(case.post_data())
