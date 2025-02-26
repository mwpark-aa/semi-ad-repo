import json
from kafka import KafkaConsumer


class MessageConsumer:
    def __init__(self, broker, topic):
        self.topic = topic
        self.broker = broker
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.broker,
            value_deserializer=lambda x: x.decode("utf-8"),
            group_id='my-group',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
        )

    def receive_message(self):
        print("Starting Kafka consumer...")
        try:
            while True:  # 무한 루프
                for message in self.consumer:
                    # 메시지 출력
                    print(f"Received message: {message.value}")

                    try:
                        data = json.loads(message.value)
                        print(f"Data indexed in Elasticsearch: {data}")
                    except json.JSONDecodeError as json_err:
                        print(f"JSON decode error: {json_err}")
                        continue

        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            self.consumer.close()

# 브로커와 토픽명을 지정한다.
broker = "localhost:9092"
topic = "info"
cs = MessageConsumer(broker, topic)
cs.receive_message()
