"""
Module is made for configuration constant served by server response

* Names of Database Columns
* Constant from dictionaires across
"""

# TODO Fetch Column names from database. Or network model. Or at least check if there is not change in contract.
# self.cursor.execute("PRAGMA table_info([sh.TestCase]);")
# names = self.cursor.fetchall()

class CaseData:
    ID = "id"
    NAME = "name"
    DESCRIPTION = "description"
    STATUS = "status"
    PRIORITY = "priority"
    OBJECTIVE = "objective"
    EXPECTED_RESULT = "expected_results"
    POST_CONDITION = "post_conditions"

    APPLICANT = "applicant"
    CREATE_TIME = "create_time"
    MODIFY_TIME = "modify_time"
    MODIFY_BY = "modify_by"
    IS_ACTIVE = "is_active"

    put = [NAME, DESCRIPTION, STATUS, PRIORITY, OBJECTIVE, EXPECTED_RESULT, POST_CONDITION, MODIFY_BY, IS_ACTIVE]
    post = [NAME, DESCRIPTION, STATUS, PRIORITY, OBJECTIVE, EXPECTED_RESULT, POST_CONDITION, APPLICANT, IS_ACTIVE]


class StepData:
    ID = "id"
    NAME = "name"
    DESCRIPTION = "description"
    ASSEMBLY = "assembly"
    TYPE = "type"

    APPLICANT = "applicant"
    CREATE_TIME = "create_time"
    MODIFY_TIME = "modify_time"
    MODIFY_BY = "modify_by"
    IS_ACTIVE = "is_active"

    put = [NAME, DESCRIPTION, ASSEMBLY, TYPE, MODIFY_BY, IS_ACTIVE]
    post = [NAME, DESCRIPTION, ASSEMBLY, TYPE, APPLICANT, IS_ACTIVE]


class CaseSteps:
    def __init__(self):
        self.ID = "id"
        self.CASE_ID = "case_id"
        self.PREVIOUS_STEP_ID = "previous_step_id"
        self.STEP_ID = "step_id"


# todo setup values according to server response
class AccountType:
    def __init__(self):
        self.__guest = 0
        self.developer = 1
        self.admin = 2
        self.__atDict = {}

    @property
    def guest(self):
        return self.__guest

    @guest.setter
    def guest(self, value):
        self.__guest = value

    @property
    def atDict(self):
        return self.__atDict

    @atDict.setter
    def atDict(self, value):
        for item in value:
            self.__atDict[item["id"]] = item["name"]


class DelatState:
    def __init__(self):
        self.__dict_states = {}
        self.close_status = 5

    @property
    def dict_state(self):
        return self.__dict_states

    @property
    def names(self):
        """
        :return: Sorted dict_state values.
        """
        return [self.__dict_states[idx] for idx in sorted(iter(self.__dict_states.keys()))]

    @property
    def names_unclose(self):
        return [self.__dict_states[idx] for idx in sorted(iter(self.__dict_states.keys())) if
                str(idx) != str(self.close_status)]

    @dict_state.setter
    def dict_state(self, value):
        """

        :param value: List of dicts [{id:X , name:N},...]
        :return:
        """
        for item in value:
            self.__dict_states[item["id"]] = item["name"]

    def state_name(self, idx):
        return self.__dict_states[str(idx)]

    def state_idx(self, search):
        try:
            return list(self.__dict_states.keys())[list(self.__dict_states.values()).index(search)]
        except ValueError:
            return ""


class Accounts:
    def __init__(self):
        self._adict = {}

        """{'notification': '1',
         'login': 'admin',
          'account_type': '2',
           'id': '1',
            'is_active': '1',
         'email': 'NULL',
          'created_datetime': '2017-06-19 11:13:23'}
          """

    @property
    def adict(self):
        return self._adict

    @adict.setter
    def adict(self, value):
        for item in value:
            self._adict[item["id"]] = item["login"]

    @property
    def names(self):
        """
        :return: Sorted dict_state values.
        """
        return [self._adict[idx] for idx in sorted(iter(self._adict.keys()))]

    def user_name(self, idx):
        return self._adict.get(str(idx), "")

    def user_idx(self, search):
        try:
            return list(self._adict.keys())[list(self._adict.values()).index(search)]
        except ValueError:
            return ""


if __name__ == '__main__':
    mydict = {1: 'Otwarte', 2: 'Przypisane', 3: 'Rozwiązane'}
    print(list(mydict.keys())[list(mydict.values()).index('Przypisane')])
else:
    atDict = AccountType()
    ds = DelatState()
    ad = Accounts()
