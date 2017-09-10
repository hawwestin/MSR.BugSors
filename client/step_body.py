from client.data_config import StepData


class StepBody:
    def __init__(self, value):
        self.data = value

        self.id = ""
        self.name = ""
        self.description = ""
        self.assembly = ""
        self.type = ""

        self.applicant = ""
        self.created_datetime = ""
        self.modify_time = ""
        self.modify_by = ""
        self.is_active = ""

        self.update(value)

    def update(self, value):
        """
        Unpack data to class attributes
        :param value: Dictionary that contains payload from Serwer.
        :return:
        """
        self.id = value.get(StepData.ID, self.id)
        self.name = value.get(StepData.NAME, self.name)
        self.description = value.get(StepData.DESCRIPTION, self.description)
        self.assembly = value.get(StepData.ASSEMBLY, self.assembly)
        self.type = value.get(StepData.TYPE, self.type)

        self.applicant = value.get(StepData.APPLICANT, self.applicant)
        self.created_datetime = value.get(StepData.CREATE_TIME, self.created_datetime)
        self.modify_time = value.get(StepData.MODIFY_TIME, self.modify_time)
        self.modify_by = value.get(StepData.MODIFY_BY, self.modify_by)
        self.is_active = value.get(StepData.IS_ACTIVE, self.is_active)

        self.data = value

    @property
    def modify_time(self):
        return self._modify_time

    @modify_time.setter
    def modify_time(self, value):
        if value is not None and value.lower() != "Null".lower():
            self._modify_time = value
        else:
            self._modify_time = ""

    def put_data(self):
        """
        format object update record in database.
        :return:
        """
        return ", ".join(["{} = '{}'".format(value, self.data.get(str(value), "null")) for value in StepData.put])

    def post_data(self):
        """
        format object in proper format to commit in DB
        :return:
        """
        return ", ".join(["'{}'".format(self.data.get(str(value), "null")) for value in StepData.post])


if __name__ == '__main__':
    data = {StepData.NAME: "lister ", StepData.ID: "1", StepData.DESCRIPTION: "descripDAWdtion", StepData.ASSEMBLY: "1",
            StepData.TYPE: "1", StepData.APPLICANT: "1", StepData.IS_ACTIVE: "true"}
    body = StepBody(data)

    print([value for value in StepData.put])
    print(body.put_data())
