from contextlib import contextmanager

import mysql.connector
import pymysql

dbconfig = {
    'user': 'user',
    'password': 'password',
    'host': 'localhost',
    'database': 'a'
}


class DBManager:
    def __init__(self):
        self.conn = None

    @contextmanager
    def get_connection(self):
        self.conn = mysql.connector.pooling.MySQLConnectionPool(
            pool_name='db_pool',
            pool_size=1,
            pool_reset_session=True,
            **dbconfig
        ).get_connection()
        yield self.conn
        self.conn.close()

    def update(self, query):
        try:
            self.conn.cursor().execute(query)
            self.conn.commit()
            return self.conn.cursor().rowcount
        except pymysql.Error:
            self.conn.rollback()
        finally:
            self.conn.cursor().close()


db_manager = DBManager()
