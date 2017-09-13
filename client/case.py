import datetime

from case_body import CaseInstance
from connection import connection
from data_config import CaseData
from data_config import StepData
from user import user

"""
Container to hold composition of CasInstances.
"""


class Case:
    def __init__(self):
        """
        Container to hold composition of CasInstances.
        """
        '''
        key - int
        value - CaseInstance
        '''
        self.delateDict = {}
        '''
        items - int CaseInstance.Id
        '''
        self.delateList = []

    def create_case_locally(self) -> CaseInstance:
        """
        Prepare new CaseInstance to be populated inside Case Tab.
        :return: CaseInstance
        """
        chunk = {CaseData.ID: 0,
                 CaseData.NAME: "Nazwa",
                 CaseData.DESCRIPTION: "Opis",
                 CaseData.APPLICANT: user.user_id,
                 CaseData.CREATE_TIME: datetime.datetime.now(),  # todo czas bez mikrosekund jest zwracany przez serwer.
                 CaseData.STATUS: 1,
                 CaseData.MODIFY_TIME: None,
                 CaseData.MODIFY_BY: None}
        self.__insert_delate_to_dict_collection(chunk)
        return self.delateDict.get(0)

    def get_case(self, idx=None):
        """
        Decode data from serwer to case that can by disposed in Class and stored in dict _delates.List.
        :param idx: pobranie wpisu z bazy o konkretnym id.
        :return:
        """
        try:
            if idx is not None and int(idx) > 0:
                items = connection.get_delate_by_id(idx)
            else:
                items = connection.get_delates()

            if len(items) == 0:
                raise AssertionError("Received payload was 0 in length")

            # if we got response from server clear dict and list and next re populate it in for loop.
            if idx is None or int(idx) == 0:
                self.delateDict.clear()
                self.delateList.clear()

            for chunk in items:
                self.__insert_delate_to_dict_collection(chunk)
        except Exception:
            raise
            # return 0
        else:
            return 1

    def __insert_delate_to_dict_collection(self, chunk: dict):
        """
        Aggregate CaseInstance in inner delateDict & DelateList.
        :param chunk: Json that holds data to populate CaseInstance
        :return:
        """
        self.delateDict[int(chunk[CaseData.ID])] = CaseInstance(chunk)
        if int(chunk[CaseData.ID]) not in self.delateList:
            self.delateList.append(int(chunk[CaseData.ID]))



    def send_new_delate(self, case: CaseInstance):
        """
        Send new instance of case to persist it in DB.
        Append added delate
        :param case:
        :return:
        """
        ret = connection.post_case(case)
        if ret != "":
            self.__insert_delate_to_dict_collection(ret[0])
            # todo clear from dict and list item with id 0 to add next item clear.
            return 1
        else:
            return 0
            # return self.get_case(ret[0].get(DD.ID, 0))

    def save_case(self, case: CaseInstance):
        """
        Send request to connection 
        :param case: 
        :return: 
        """
        connection.put_case(case)
        return self.get_case(case.id)


if __name__ == '__main__':
    pass
else:
    case_collection = Case()
