import datetime

from data_config import dd
from data_config import dc
from network import con
from user import user
from delate_body import DelateInstance


class Delates:
    def __init__(self):
        self.delateDict = {}
        self.delateList = []

    def create_delate_localy(self):
        chunk = {dd.ID: 0,
                 dd.NAME: "Nazwa",
                 dd.DESCRIPTION: "Opis",
                 dd.APPLICANT: user.user_id,
                 dd.ASSIGNED: "",
                 dd.CREATE_TIME: datetime.datetime.now(),# todo czas bez mikrosekund jest zwracany przez serwer.
                 dd.STATUS: 1,
                 dd.MODIFY_TIME: None,
                 dd.MODIFY_BY: None}
        self.__insert_delate_to_dict_collection(chunk)
        return self.delateDict.get(0)

    def get_delate(self, idx=None):
        """
        Decode data from serwer to delates that can by didposed in Class and stored in dict _delates.List.
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
        Aggregate DelateInstance in inner delateDict & DelateList.
        :param chunk: Json that holds data to populate DelateInstance
        :return:
        """
        item = DelateInstance(id=chunk[dd.ID],
                              name=chunk[dd.NAME],
                              desc=chunk[dd.DESCRIPTION],
                              app=chunk[dd.APPLICANT],
                              ass=chunk[dd.ASSIGNED],
                              create=chunk[dd.CREATE_TIME],
                              stat=chunk[dd.STATUS],
                              mtime=chunk[dd.MODIFY_TIME],
                              mby=chunk[dd.MODIFY_BY])
        item.aggregated = chunk
        self.delateDict[int(chunk[dd.ID])] = item
        if int(chunk[dd.ID]) not in self.delateList:
            self.delateList.append(int(chunk[dd.ID]))

    def DecodeComment(self, idx):
        """
        Decode data from serwer to comments that can by displayed on UI

        There should by a delate to coresponding comment.
        :param idx:
        :return:
        """
        items = con.get_comments(idx)

        for item in items:
            self.delateDict[idx].dictComments[item[dc.ID]] = items

    def send_new_delate(self, delate):
        """
        Send new instance of delate to presist it in DB.
        Append added delate
        :param delate:
        :return:
        """
        ret = con.post_delate(delate)
        if ret != "":
            self.__insert_delate_to_dict_collection(ret[0])
            return 1
        else:
            return 0
            # return self.get_delate(ret[0].get(DD.ID, 0))

    def save_delate(self, delate):
        con.put_delate(delate)
        return self.get_delate(delate.id)


if __name__ == '__main__':
    date = datetime.datetime.utcnow()
    print(date.isoformat())
    print(date.ctime())
    print(date.utcnow())
    print(date.utctimetuple())
    print("{} {}".format(date.date(), date.timestamp()))
else:
    delates = Delates()
