import datetime

from data_config import CaseData
from data_config import StepData
from network import con
from user import user
from case_body import CaseInstance


class Case:
    def __init__(self):
        self.delateDict = {}
        self.delateList = []

    def create_case_locally(self):
        chunk = {CaseData.ID: 0,
                 CaseData.NAME: "Nazwa",
                 CaseData.DESCRIPTION: "Opis",
                 CaseData.APPLICANT: user.user_id,
                 CaseData.ASSIGNED: "",
                 CaseData.CREATE_TIME: datetime.datetime.now(),# todo czas bez mikrosekund jest zwracany przez serwer.
                 CaseData.STATUS: 1,
                 CaseData.MODIFY_TIME: None,
                 CaseData.MODIFY_BY: None}
        self.__insert_delate_to_dict_collection(chunk)
        return self.delateDict.get(0)

    def get_delate(self, idx=None):
        """
        Decode data from serwer to case that can by didposed in Class and stored in dict _delates.List.
        :param idx: pobranie wpisu z bazy o konkretnym id.
        :return:
        """
        try:
            if idx is not None and int(idx) > 0:
                items = con.get_delate_by_id(idx)
            else:
                items = con.get_delates()

            if len(items) == 0:
                return 0

            if idx is None or int(idx) == 0:
                self.delateDict.clear()
                self.delateList.clear()

            for chunk in items:
                self.__insert_delate_to_dict_collection(chunk)
        except Exception:
            return 0
        else:
            return 1

    def __insert_delate_to_dict_collection(self, chunk):
        """
        Aggregate CaseInstance in inner delateDict & DelateList.
        :param chunk: Json that holds data to populate CaseInstance
        :return:
        """
        item = CaseInstance(id=chunk[CaseData.ID],
                            name=chunk[CaseData.NAME],
                            desc=chunk[CaseData.DESCRIPTION],
                            app=chunk[CaseData.APPLICANT],
                            ass=chunk[CaseData.ASSIGNED],
                            create=chunk[CaseData.CREATE_TIME],
                            stat=chunk[CaseData.STATUS],
                            mtime=chunk[CaseData.MODIFY_TIME],
                            mby=chunk[CaseData.MODIFY_BY])
        item.aggregated = chunk
        self.delateDict[int(chunk[CaseData.ID])] = item
        if int(chunk[CaseData.ID]) not in self.delateList:
            self.delateList.append(int(chunk[CaseData.ID]))

    def DecodeComment(self, idx):
        """
        Decode data from serwer to steps that can by displayed on UI

        There should by a delate to coresponding comment.
        :param idx:
        :return:
        """
        items = con.get_steps(idx)

        for item in items:
            self.delateDict[idx].dictComments[item[StepData.ID]] = items

    def send_new_delate(self, delate):
        """
        Send new instance of delate to presist it in DB.
        Append added delate
        :param delate:
        :return:
        """
        ret = con.post_case(delate)
        if ret != "":
            self.__insert_delate_to_dict_collection(ret[0])
            return 1
        else:
            return 0
            # return self.get_delate(ret[0].get(DD.ID, 0))

    def save_delate(self, delate):
        con.put_case(delate)
        return self.get_delate(delate.id)


if __name__ == '__main__':
    date = datetime.datetime.utcnow()
    print(date.isoformat())
    print(date.ctime())
    print(date.utcnow())
    print(date.utctimetuple())
    print("{} {}".format(date.date(), date.timestamp()))
else:
    case = Case()
