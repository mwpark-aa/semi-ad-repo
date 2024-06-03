from abc import ABC, abstractmethod
from contextlib import contextmanager

import mysql.connector
import pymysql
import redis

db_config = {
    'user': 'user',
    'password': 'password',
    'host': 'localhost',
    'database': 'a'
}

redis_config = {
    'host': 'localhost',
    'port': 6379,
    'decode_responses': True,
}


class DBManager(ABC):
    def __init__(self):
        self.conn = None

    @abstractmethod
    def get_connection(self):
        pass



class MySQLManager(DBManager):

    def __init__(self):
        super().__init__()

    @contextmanager
    def get_connection(self):
        self.conn = mysql.connector.pooling.MySQLConnectionPool(
            pool_name='db_pool',
            pool_size=1,
            pool_reset_session=True,
            **db_config
        ).get_connection()
        try:
            yield self.conn
        finally:
            if self.conn:
                self.conn.close()

    def update(self, query):
        with self.get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                return cursor.rowcount
            except mysql.connector.Error:
                conn.rollback()
            finally:
                cursor.close()


class RedisManager(DBManager):

    def __init__(self):
        super().__init__()

    @contextmanager
    def get_connection(self):
        self.conn = redis.Redis(**redis_config)
        try:
            yield self.conn
        finally:
            if self.conn:
                self.conn.close()

    def update(self, key, value):
        with self.get_connection() as conn:
            conn.set(key, value)


redis_manager = RedisManager()
mysql_manager = MySQLManager()
