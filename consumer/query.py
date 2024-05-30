import pymysql


def insert_kafka(conn, value):
    query = f'''
    INSERT INTO admin (kafka_num) VALUES ('{value}');
    '''
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
    except pymysql.Error as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
