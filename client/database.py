import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("test.db")
        self.cursor = self.connection.cursor()


    def prepare_db(self):
        """
        Prepare database schema to hold ours data i local DB.
        :return:
        """
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS delates \n"
            "(id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, isbn INTEGER)\n")
        self.connection.commit()


if __name__ == '__main__':
    pass
else:
    database = Database()
