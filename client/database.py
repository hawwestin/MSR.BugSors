import sqlite3
import os.path
from connections import ConnectBase
from data_config import StepData


class Database(ConnectBase):

    def __init__(self):
        self.connection = None
        self.cursor = None

    def configure(self, **kwargs):
        db_path = kwargs.get('adres', "../db/test_local.db")
        if os.path.isfile(db_path):
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
        else:
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
            self.prepare_db()
        #     create user in empty database.

        self.connection.execute("PRAGMA FOREIGN_KEYS =1")

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
        except FileNotFoundError:
            # todo statusbar Logger
            pass
        except IOError:
            # todo statusbar Logger
            pass

    def put_step(self, step):
        """
        Update step
        :param step: StepBody object
        :return:
        """
        sql = "UPDATE [sh.Step] SET {} WHERE {}"
        values = step.put_data()

        sql = sql.format(values, "{} = '{}'".format(StepData.ID, step.id))

        print(sql) # todo logger.

        try:
            self.cursor.executescript(sql)
        except sqlite3.IntegrityError:
            # todo statusbar logger
            raise
        else:
            self.connection.commit()

    def get_delate_by_applicant(self, idx):
        sql = ""
        self.cursor.executescript(sql)
        self.connection.commit()

    def get_delate_by_assign(self, idx):
        sql = ""
        self.cursor.executescript(sql)
        self.connection.commit()

    def get_delate_by_id(self, idx):
        sql = ""
        self.cursor.executescript(sql)
        self.connection.commit()

    def put_case(self, case):
        sql = ""
        self.cursor.executescript(sql)
        self.connection.commit()

    def get_steps(self, idx):
        sql = ""
        self.cursor.executescript(sql)
        self.connection.commit()

    def get_dict_states(self):

        sql = ""
        self.cursor.executescript(sql)
        self.connection.commit()

    def post_case(self, case):
        # ////
        sql = "INSERT INTO [sh.TestCase] ({0}) VALUES ({1});"
        values = case.post_data()

        self.cursor.executescript(sql)
        self.connection.commit()

    def login(self):
        sql = ""
        self.cursor.executescript(sql)
        self.connection.commit()

    def get_delates(self, **kwargs):
        sql = ""
        self.cursor.executescript(sql)
        self.connection.commit()

    def get_users(self):
        sql = ""
        self.cursor.executescript(sql)
        self.connection.commit()

    def post_step(self, step):
        sql = "INSERT INTO [sh.Step] ({0})VALUES ({1});"
        values = step.post_data()

        sql = sql.format(', '.join(StepData.post), values)

        # print(sql) todo logger.
        try:
            self.cursor.executescript(sql)
        except sqlite3.IntegrityError:
            # todo statusbar logger
            raise
        else:
            self.connection.commit()

    def add_user(self, user):
        pass


if __name__ == '__main__':
    from step_body import StepBody, StepData
    db = Database()
    db.configure()
    data = {}
    data[StepData.NAME] = "lister "
    data[StepData.ID] = "2"
    data[StepData.DESCRIPTION] = "descripDAWdtion"
    data[StepData.ASSEMBLY] = "1"
    data[StepData.TYPE] = "1"
    data[StepData.APPLICANT] = "1"
    data[StepData.MODIFY_BY] = "1"
    data[StepData.IS_ACTIVE] = "true"
    body = StepBody(data)
    db.put_step(body)
else:
    database = Database()
