import os.path
import sqlite3
import pathlib

from client.connection_module.connect_base import ConnectBase
from client.data_config import CaseData, CaseSteps, Accounts, BasicSHDict
from client.data_config import StepData
from client.user import user


class Database(ConnectBase):
    def __init__(self, **kwargs):
        '''
        API to communicate with local instance of database.
        :param kwargs:
            adres : path to database file.
        '''
        self.connection = None
        self.cursor = None
        self.db_path = None
        self.configure(kwargs.get('adres', "../db/test_local.db"))

    def configure(self, adres):
        self.db_path = adres
        try:
            if os.path.isfile(self.db_path):
                print("File found opening DB in {}".format(adres))
                self.connection = sqlite3.connect(self.db_path)
                self.cursor = self.connection.cursor()
            else:
                print("File not found create new DB in {}".format(adres))
                self.connection = sqlite3.connect(self.db_path)
                self.cursor = self.connection.cursor()
                self.prepare_db()
        except FileNotFoundError:
            # todo statusbar Logger
            raise
        except IOError:
            # todo statusbar Logger
            raise
        self.connection.execute("PRAGMA FOREIGN_KEYS = 1")

    def __del__(self):
        if self.connection is not None:
            self.connection.close()

    def prepare_db(self):
        """
        Prepare database schema to hold ours data i local DB.
        :return:
        """
        try:
            if os.path.isfile("../db/schema.sql"):
                with open("../db/schema.sql", 'r') as file:
                    init_sql = file.read()
                self.cursor.executescript(init_sql)
                self.connection.commit()
                # todo create user in empty database add user to schema or prompt to create wia new window.
        except FileNotFoundError:
            # todo statusbar Logger
            raise
        except IOError:
            # todo statusbar Logger
            raise

    def _read_data(self, request):
        """
        Create a list of dictionaries column name : value per fetched row.
        :param request: List of tuples returned from database.
        :return: JSON list of dictionaries column name : value per row
        """
        if request is not None and len(request) > 0:
            names = [description[0] for description in self.cursor.description]
            ret_val = []
            for tup in request:
                ret_val.append(dict(zip(names, tup)))
            print(ret_val)
            return ret_val
        else:
            # todo logging and status bar message
            return ''

    def put_step(self, step):
        sql = "UPDATE [sh.Step] SET {} WHERE {}"
        sql = sql.format(step.put_data(), "{} = '{}'".format(StepData.ID, step.id))

        try:
            self.cursor.executescript(sql)
        except sqlite3.IntegrityError:
            # todo statusbar logger
            raise
        else:
            self.connection.commit()

    def get_case_by_applicant(self, idx):
        sql = """SELECT * FROM [sh.TestCase] WHERE {} ={}"""
        sql = sql.format(CaseData.APPLICANT, str(idx))
        print(sql)
        try:
            self.cursor.execute(sql)
        except sqlite3.OperationalError:
            raise
        return self._read_data(self.cursor.fetchall())

    def get_case_by_id(self, idx):
        sql = """SELECT * FROM [sh.TestCase] WHERE {} ={}"""
        sql = sql.format(CaseData.ID, str(idx))
        print(sql)
        try:
            self.cursor.execute(sql)
        except sqlite3.OperationalError:
            raise
        return self._read_data(self.cursor.fetchall())

    def put_case(self, case):
        sql = "UPDATE [sh.TestCase] SET {} WHERE {}"
        sql = sql.format(case.put_data(), "{} = '{}'".format(CaseData.ID, case.id))
        print(sql)
        try:
            self.cursor.executescript(sql)
        except sqlite3.IntegrityError:
            # todo statusbar logger
            raise
        else:
            self.connection.commit()

    def get_steps(self, case_id):
        sql = "SELECT * FROM [sh.CaseSteps] where {} = {}"
        sql = sql.format(CaseSteps.CASE_ID, str(case_id))
        print(sql)
        try:
            self.cursor.execute(sql)
        except sqlite3.OperationalError:
            raise
        return self._read_data(self.cursor.fetchall())

    def get_step(self, step_id) -> dict:
        sql = "SELECT * FROM [sh.Step] where {} = {}"
        sql = sql.format(StepData.ID, str(step_id))
        print(sql)
        try:
            self.cursor.execute(sql)
        except sqlite3.OperationalError:
            raise
        return self._read_data(self.cursor.fetchall())[0]

    def get_dict(self, dict_type: BasicSHDict):
        if dict_type.TABLE is None:
            raise AttributeError("Table name unknown")
        sql = """SELECT {}, {} FROM [{}]"""
        sql = sql.format(dict_type.ID, dict_type.NAME, dict_type.TABLE)
        print(sql)
        try:
            self.cursor.execute(sql)
        except sqlite3.OperationalError:
            raise
        return self._read_data(self.cursor.fetchall())

    def post_case(self, case):
        sql = "INSERT INTO [sh.TestCase] ({0}) VALUES ({1});"
        values = case.post_data()

        sql = sql.format(', '.join(CaseData.post), values)
        print(sql)
        try:
            self.cursor.execute(sql)
        except sqlite3.IntegrityError:
            # todo statusbar logger
            raise
        else:
            self.connection.commit()

    def authenticate(self) -> bool:
        """
        Check if user exist and password matches
        :return:
        """
        sql = """SELECT count(ALL) FROM [sh.Users] where {} like '{}' and {} like '{}'"""
        sql = sql.format(Accounts.LOGIN, user.login, Accounts.PASSWORD, user.password)
        print(sql)
        try:
            self.cursor.execute(sql)
        except sqlite3.OperationalError:
            raise
        return str(self._read_data(self.cursor.fetchall())[0].get('count(ALL)', "0")) == "1"

    def _token(self):
        """
        Menage token and refresh token. in local connection may by empty.
        :return:
        """
        pass

    def login(self):
        if self.authenticate():
            sql = """SELECT {}, {}, {} FROM [sh.Users] where {} like '{}'"""
            sql = sql.format(Accounts.ID, Accounts.TOKEN, Accounts.Account_TYPE, Accounts.LOGIN, user.login)
            print(sql)
            try:
                self.cursor.execute(sql)
            except sqlite3.OperationalError:
                raise
            return self._read_data(self.cursor.fetchall())[0]
        raise UserWarning("invalid login data.")

    def get_case(self):
        sql = """SELECT * FROM [sh.TestCase]"""
        print(sql)
        try:
            self.cursor.execute(sql)
        except sqlite3.OperationalError:
            raise
        return self._read_data(self.cursor.fetchall())

    def post_step(self, step):
        sql = "INSERT INTO [sh.Step] ({0})VALUES ({1});"
        values = step.post_data()

        sql = sql.format(', '.join(StepData.post), values)

        # print(sql) todo logger.
        try:
            self.cursor.execute(sql)
        except sqlite3.IntegrityError:
            # todo statusbar logger
            raise
        else:
            self.connection.commit()

    def add_user(self, user):
        pass


if __name__ == '__main__':
    # from step_body import StepBody, StepData
    from case_body import CaseInstance

    db = Database(adres="../../db/test_local.db")
    # data = {}
    # data[StepData.NAME] = "lister "
    # data[StepData.ID] = "2"
    # data[StepData.DESCRIPTION] = "descripDAWdtion"
    # data[StepData.ASSEMBLY] = "1"
    # data[StepData.TYPE] = "1"
    # data[StepData.APPLICANT] = "1"
    # data[StepData.MODIFY_BY] = "1"
    # data[StepData.IS_ACTIVE] = "true"
    # body = StepBody(data)
    # db.put_step(body)
    # data = {}
    # data[CaseData.ID] = '5'
    # data[CaseData.NAME] = 'name3'
    # data[CaseData.DESCRIPTION] = 'desc23'
    # data[CaseData.STATUS] = '1'
    # data[CaseData.PRIORITY] = '1'
    # data[CaseData.OBJECTIVE] = 'obj2'
    # data[CaseData.EXPECTED_RESULT] = 'exp23'
    # data[CaseData.POST_CONDITION] = 'post cond23'
    # data[CaseData.MODIFY_BY] = '2'
    # data[CaseData.IS_ACTIVE] = 'true'
    # case = CaseInstance(data)
    # db.put_case(case)
    user.login = "robaszew"
    user.password = "truecrypt"

    print(db.authenticate())


else:
    pass
