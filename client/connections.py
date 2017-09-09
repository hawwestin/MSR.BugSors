import abc


class ConnectBase(metaclass=abc.ABCMeta):
    """
    Base class for connection to remote server and to local database.

    """
    @classmethod
    def __subclasshook__(cls, C):
        if cls is ConnectBase:
            attrs = set(dir(C))
            if set(cls.__abstractmethods__) <= attrs:
                return True
        return NotImplemented

    @abc.abstractmethod
    def configure(self, **kwargs):
        pass

    @abc.abstractmethod
    def get_dict_stats(self):
        pass

    @abc.abstractmethod
    def get_delates(self, **kwargs):
        pass

    @abc.abstractmethod
    def get_delates_by_id(self, idx):
        pass
