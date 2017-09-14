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
        '''
        Valid kw :
            adres - place with to connect

        :param kwargs:
        :return:
        '''
        pass

    @abc.abstractmethod
    def get_dict_states(self):
        pass

    @abc.abstractmethod
    def get_delates(self, **kwargs):
        pass

    @abc.abstractmethod
    def get_delate_by_id(self, idx):
        pass

    @abc.abstractmethod
    def login(self):
        pass

    @abc.abstractmethod
    def get_case_by_applicant(self, idx):
        pass

    @abc.abstractmethod
    def get_delate_by_assign(self, idx):
        pass

    @abc.abstractmethod
    def get_steps(self, case_id):
        """
        Get steps bound to given case
        :param case_id:
        :return:
        """
        pass

    @abc.abstractmethod
    def get_step(self, step_id) -> dict:
        """
        Get single Step from connection
        :param step_id:
        :return:
        """
        pass

    @abc.abstractmethod
    def put_case(self, case):
        """
        Update case
        :param case:
        :return:
        """
        pass

    @abc.abstractmethod
    def post_case(self, case):
        """
        Insert new case
        :param case:
        :return:
        """
        pass

    @abc.abstractmethod
    def post_step(self, step):
        """
        Insert new step
        :param step:
        :return:
        """
        pass

    @abc.abstractmethod
    def put_step(self, step):
        """
        Update step
        :param step:
        :return:
        """
        pass

    @abc.abstractmethod
    def get_users(self):
        pass

    @abc.abstractmethod
    def add_user(self, user):
        pass