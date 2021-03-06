"""
Module is made for configuration constant served by server response

* Names of Database Columns
* Constant from dictionaries across application.
"""


# TODO Fetch Column names from database. Or network model. Or at least check if there is not change in contract.
# self.cursor.execute("PRAGMA table_info([sh.TestCase]);")
# names = self.cursor.fetchall()
# todo add table name to class.


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
    ID = "id"
    CASE_ID = "case_id"
    PREVIOUS_STEP_ID = "previous_step_id"
    STEP_ID = "step_id"


#####################
# ==================== Dictionaries
#####################


class BasicSHDict:
    ID = 'id'
    NAME = 'name'
    TABLE = ''

    def __init__(self):
        self._data = {}

    @property
    def data(self):
        """
        dict of id : name
        :return:
        """
        return self._data

    @data.setter
    def data(self, value):
        """

        :param value: value: List of dicts [{id:X , name:N},...]
        :return:
        """
        try:
            for item in value:
                self._data[str(item[self.ID])] = item[self.NAME]
        except KeyError:
            # todo log
            raise

    @property
    def names(self) -> list:
        """
        :return: Sorted data values by keys.
        """
        return [self.data[idx] for idx in sorted(iter(self.data.keys()))]

    def index(self, search):
        """
        For given dict name search id.
        :param search:
        :return:"""
        try:
            return list(self.data.keys())[list(self.data.values()).index(search)]
        except ValueError:
            return ""

    def get_name(self, idx):
        return self.data.get(str(idx), "")


class Accounts(BasicSHDict):
    TABLE = "sh.Users"
    ID = "id"
    NAME = "full_name"
    LOGIN = "login"
    Account_TYPE = "account_type"
    PASSWORD = "password"
    TOKEN = "token"
    IS_ACTIVE = "is_active"
    EMAIL = "email"

    put = [ID, NAME, LOGIN, Account_TYPE, PASSWORD, EMAIL]
    post = [NAME, LOGIN, Account_TYPE, PASSWORD, EMAIL]


# todo setup values according to server response
class AccountType(BasicSHDict):
    TABLE = 'sh.dict.AccountType'

    def __init__(self):
        self.__guest = 0
        self.developer = 1
        self.admin = 2
        super().__init__()

    @property
    def guest(self):
        return self.__guest

    @guest.setter
    def guest(self, value):
        self.__guest = value


class CaseStatus(BasicSHDict):
    TABLE = 'sh.dict.CaseStatus'
    pass


class CasePriority(BasicSHDict):
    TABLE = 'sh.dict.Priority'
    pass


class StepAssembly(BasicSHDict):
    TABLE = 'sh.dict.StepAssembly'
    pass


class StepType(BasicSHDict):
    TABLE = 'sh.dict.StepType'
    pass


if __name__ == '__main__':
    mydict = {1: 'Otwarte', 2: 'Przypisane', 3: 'Rozwiązane'}
    print(list(mydict.keys())[list(mydict.values()).index('Przypisane')])
else:
    dict_account_type = AccountType()
    dict_case_status = CaseStatus()
    dict_accounts = Accounts()
    dict_priority = CasePriority()
    dict_step_assembly = StepAssembly()
    dict_step_type = StepType()
