from kafka import KafkaConsumer

from db.query import insert_data
from db.repository import mysql_manager, redis_manager


class MessageConsumer:
    def __init__(self, broker, topic):
        self.topic = topic
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
        # mysql 로 insert
        # with mysql_manager.get_connection():
        #     for message in self.consumer:
        #         query = insert_data(self.topic, message.value)
        #         mysql_manager.update(query=query)

        # redis 로 insert
        with redis_manager.get_connection():
            for message in self.consumer:
                redis_manager.update(update_data=message.value)


# 브로커와 토픽명을 지정한다.
broker = ["localhost:9092"]
topic = "my-topic"
cs = MessageConsumer(broker, topic)
cs.receive_message()