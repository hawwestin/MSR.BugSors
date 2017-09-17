from client.data_config import dict_account_type


class User:
    """
    simple user management class for authenticate in current connection.
    """
    def __init__(self):
        self.login = ""
        self.__password = ""
        self.token = ""
        self.user_id = ""
        self.user_type = dict_account_type.guest

    @property
    def password(self):
        """
        return secure format of pass
        :return:
        """
        return self.__password

    @password.setter
    def password(self, value):
        """
        set secure format of password
        :param value:
        :return:
        """
        # todo hash value password to store it in secure way
        self.__password = value

    def is_logged_in(self):
        return self.login != "" or self.password != "" or self.token != ""


if __name__ == '__main__':
    pass
else:
    user = User()
