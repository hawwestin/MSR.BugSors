from data_config import atDict


class User:
    def __init__(self):
        self.login = ""
        self._password = ""
        self.token = ""
        self.user_id = ""
        self.user_type = atDict.guest

    @property
    def password(self):
        """
        return secure format of pass
        :return:
        """
        return self._password

    @password.setter
    def password(self, value):
        """
        set secure format of password
        :param value:
        :return:
        """
        self._password = value

    def is_logged_in(self):
        return self.login == "" or self.password == "" or self.token == ""


if __name__ == '__main__':
    pass
else:
    user = User()
