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
            print(e)

        return conn

    def post(self, sql):
        try:
            print(sql)
            conn = self.create_connection()
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            print("Total", cur.rowcount, "Records inserted successfully into SqliteDb_developers table")
            conn.commit()
            cur.close()
        except sqlite3.Error as error:
            print(error)
            print("Failed to insert record into sqlite table", error)
        finally:
            if (conn):
                conn.close()
                print("The SQLite connection is closed")

    def post_many(self, sql, items=None):
        try:
            conn = self.create_connection()
            cur = conn.cursor()
            if items:
                cur.executemany(sql, items)
            else:
                for query in sql:
                    try:
                        cur.execute(query)
                        conn.commit()
                    except sqlite3.Error as e:
                        continue
                conn.commit()
            print(f"Total {len(sql)} Records inserted successfully into SqliteDb_developers table")
            conn.commit()
            cur.close()
        except sqlite3.Error as error:
            print("Failed to insert multiple records into sqlite table", error)
        finally:
            if (conn):
                conn.close()
                print("The SQLite connection is closed")

    def get(self, sql):
        try:
            conn = self.create_connection()
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if(conn):
                conn.close()
                print("The SQLite connection is closed")
        return [row[0] for row in rows]