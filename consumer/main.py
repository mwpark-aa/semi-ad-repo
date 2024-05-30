import mysql
from kafka import KafkaConsumer

from query import insert_kafka
from repository import get_db_conn


class MessageConsumer:
    def __init__(self, broker, topic):
        self.broker = broker
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.broker,
            value_deserializer=lambda x: x.decode("utf-8"),
            group_id='my-group',
            auto_offset_reset='latest',
            enable_auto_commit=True,
        )

    def receive_message(self):
        conn = get_db_conn()
        try:
            for message in self.consumer:
                insert_kafka(conn, message.value)
        except mysql.connector.Error:
            conn = get_db_conn()
        except Exception as exc:
            raise exc
        finally:
            conn.close()


# 브로커와 토픽명을 지정한다.
broker = ["localhost:9092"]
topic = "my-topic"
cs = MessageConsumer(broker, topic)
cs.receive_message()