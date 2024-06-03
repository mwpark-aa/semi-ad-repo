from abc import ABC, abstractmethod
from contextlib import contextmanager

import mysql.connector
import pymysql
import redis
import json

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
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            self.conn.commit()
            return cursor.rowcount
        except mysql.connector.Error:
            self.conn.rollback()
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
        self.conn.set(key, value)

    def update(self, update_data):
        if isinstance(update_data, str):
            try:
                dict_data = json.loads(update_data)
            except json.decoder.JSONDecodeError:
                raise ValueError("Invalid JSON")
        elif isinstance(update_data, dict):
            dict_data = update_data
        else:
            raise ValueError('Update data must be dict or str')

        for key, value in dict_data.items():
            try:
                self.conn.set(key, value)
            except Exception as e:
                print('error occured when update redis' + e)
                continue


redis_manager = RedisManager()
mysql_manager = MySQLManager()
