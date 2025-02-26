from kafka import KafkaProducer
import json


class MessageProducer:
    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=self.broker,
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
            acks='all',
            api_version=(2, 5, 0),
            retries=3,
        )

    def send_message(self, msg, auto_close=False):
        try:
            future = self.producer.send(self.topic, msg)
            print(future.get())
            self.producer.flush()  # 비우는 작업
            if auto_close:
                self.producer.close()
            future.get(timeout=2)
        except Exception as exc:
            raise exc