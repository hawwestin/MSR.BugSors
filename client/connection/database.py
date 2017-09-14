import os.path
import sqlite3
import pathlib

from connection.connect_base import ConnectBase
from data_config import CaseData, CaseSteps
from data_config import StepData
from step_body import StepBody


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
        # create user in empty database.
        try:
            if os.path.isfile("../db/schema.sql"):
                with open("../db/schema.sql", 'r') as file:
                    init_sql = file.read()
                self.cursor.executescript(init_sql)
                self.connection.commit()
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

    def get_delate_by_assign(self, idx):
        sql = ""
        self.cursor.execute(sql)
        self.connection.commit()

    def get_delate_by_id(self, idx):
        sql = """SELECT * FROM [sh.TestCase] WHERE {} ={}"""
        sql = sql.format(CaseData.ID, str(idx))
        print(sql)
        try:
            self.cursor.execute(sql)
        except sqlite3.OperationalError:
            raise
        return self._read_data(self.cursor.fetchall())

    def put_case(self, case):
        sql = ""
        self.cursor.execute(sql)
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

    def get_dict_states(self):

        sql = ""
        self.cursor.execute(sql)
        self.connection.commit()

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

    def login(self):
        # sql = ""
        # self.cursor.execute(sql)
        # self.connection.commit()
        return {"token": "a", "user_account_type": 1, "user_id": 1}

    def get_delates(self, **kwargs):
        sql = ""
        self.cursor.execute(sql)
        self.connection.commit()

    def get_users(self):
        sql = ""
        self.cursor.execute(sql)
        self.connection.commit()

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
    from case_body import CaseInstance

    db_file = pathlib.Path()
    print(db_file.cwd())

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
    # data[CaseData.ID] = '1'
    # data[CaseData.NAME] = 'name3'
    # data[CaseData.DESCRIPTION] = 'desc23'
    # data[CaseData.STATUS] = '1'
    # data[CaseData.PRIORITY] = '1'
    # data[CaseData.OBJECTIVE] = 'obj2'
    # data[CaseData.EXPECTED_RESULT] = 'exp23'
    # data[CaseData.POST_CONDITION] = 'post cond23'
    # data[CaseData.APPLICANT] = '1'
    # data[CaseData.IS_ACTIVE] = '1'
    # case = CaseInstance(data)
    # db.post_case(case)

else:
    pass
