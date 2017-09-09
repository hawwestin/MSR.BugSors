"""
Module is made for configuration constant served by server response

* Names of Database Columns
* Constant from dictionaires across
"""


class DelateData:
    def __init__(self):
        self.MODIFY_BY = "modify_by"
        self.ID = "id"
        self.APPLICANT = "applicant"
        self.DESCRIPTION = "description"
        self.CREATE_TIME = "create_time"
        self.STATUS = "status"
        self.NAME = "name"
        self.ASSIGNED = "assigned"
        self.MODIFY_TIME = "modify_time"


class CommentData:
    def __init__(self):
        self.APPLICANT = "applicant"
        self.IS_ACTIVE = "is_active"
        self.CREATED_DT = "created_datetime"
        self.DELATE_ID = "delate_id"
        self.COMMENT = "comment"
        self.ID = "id"
        self.MODIFY_TIME = "modify_time"


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
    dd = DelateData()
    dc = CommentData()
    atDict = AccountType()
    ds = DelatState()
    ad = Accounts()
