import sqlite3
from sqlite3 import Error

class sqlite:
    def __init__(self, db_file):
        self.db = db_file

    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db)
            print(conn)
        except Error as e:
            print('Are we in here?')
            print(e)

        return conn


    def post_many(self, sql, items):
        try:
            conn = self.create_connection()
            cur = conn.cursor()
            cur.executemany(sql, items)
            conn.commit()
            print("Total", cur.rowcount, "Records inserted successfully into SqliteDb_developers table")
            conn.commit()
            cur.close()
        except sqlite3.Error as error:
            print("Failed to insert multiple records into sqlite table", error)
        finally:
            if (conn):
                conn.close()
                print("The SQLite connection is closed")
