from .database import Database
from .network import ServerConnection
from .connect_base import ConnectBase


class Connection:
    def __init__(self):
        self.__connection = None

    @property
    def connection(self) -> ConnectBase:
        return self.__connection

    @connection.setter
    def connection(self, value):
        if isinstance(value, ConnectBase):
            self.__connection = value
        else:
            raise ValueError("Not valid connection class")


if __name__ == '__main__':
    pass
else:
    com_switch = Connection()
