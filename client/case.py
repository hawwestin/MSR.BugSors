import datetime

from client.case_body import CaseBody
from client.connection_module import com_switch
from client.data_config import CaseData
from client.user import user

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
        value - CaseBody
        '''
        self.delateDict = {}
        '''
        items - int CaseBody.Id
        '''
        self.delateList = []

    def create_case_locally(self) -> CaseBody:
        """
        Prepare new CaseBody to be populated inside Case Tab.
        :return: CaseBody
        """
        chunk = {CaseData.ID: 0,
                 CaseData.NAME: "Nazwa",
                 CaseData.DESCRIPTION: "Opis",
                 CaseData.APPLICANT: user.user_id,
                 CaseData.CREATE_TIME: datetime.datetime.now(),  # todo czas bez mikrosekund jest zwracany przez serwer.
                 CaseData.STATUS: "1",
                 CaseData.PRIORITY: "2",
                 CaseData.MODIFY_TIME: None,
                 CaseData.MODIFY_BY: None,
                 CaseData.IS_ACTIVE: True}
        self.__insert_delate_to_dict_collection(chunk)
        return self.delateDict.get(0)

    def fetch_case(self, idx=None):
        """
        Decode data from serwer to case that can by disposed in Class and stored in dict _delates.List.
        :param idx: pobranie wpisu z bazy o konkretnym id.
        :return:
        """
        try:
            if idx is not None and int(idx) > 0:
                items = com_switch.connection.get_case_by_id(idx)
            else:
                items = com_switch.connection.get_case()

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
        Aggregate CaseBody in inner delateDict & DelateList.
        :param chunk: Json that holds data to populate CaseBody
        :return:
        """
        self.delateDict[int(chunk[CaseData.ID])] = CaseBody(**chunk)
        if int(chunk[CaseData.ID]) not in self.delateList:
            self.delateList.append(int(chunk[CaseData.ID]))



    def send_new_delate(self, case: CaseBody):
        """
        Send new instance of case to persist it in DB.
        Append added delate
        :param case:
        :return:
        """
        ret = com_switch.connection.post_case(case)
        ret = com_switch.connection.get_case_by_id(ret)
        if ret != "":
            self.__insert_delate_to_dict_collection(ret[0])
            # todo clear from dict and list item with id 0 to add next item clear.
            return 1
        else:
            return 0
            # return self.fetch_case(ret[0].get(DD.ID, 0))

    def save_case(self, case: CaseBody):
        """
        Send request to connection 
        :param case: 
        :return: 
        """
        com_switch.connection.put_case(case)
        return self.fetch_case(case.id)


if __name__ == '__main__':
    pass
else:
    case_collection = Case()
