import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool


dbconfig = {
    'user': 'user',
    'password': 'password',
    'host': 'localhost',
    'database': 'a'
}

def get_db_conn():
    conn = mysql.connector.pooling.MySQLConnectionPool(
        pool_name='db_pool',
        pool_size=1,
        pool_reset_session=True,
        **dbconfig
    )
    return conn.get_connection()
