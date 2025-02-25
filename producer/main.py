import time

from fastapi import FastAPI

from producer import MessageProducer

app = FastAPI()

broker = ["localhost:9092"]

@app.get("/click/{user_id}")
def click(user_id: str):
    topic = "info"
    sender = MessageProducer(broker, topic)
    message = {f'user_{user_id}': {"click": 1}}
    sender.send_message(message)
    print(f'send message: {message}')


@app.get("/impression/{user_id}")
def click(user_id: str):
    topic = "info"
    sender = MessageProducer(broker, topic)
    message = {f'user_{user_id}': {"impression": 1}}
    sender.send_message(message)
    print(f'send message: {message}')


@app.get("/ad")
def get_ad(media_id: int, zone_id: int):
    # zone (영역) 정보를 가지고옴
    print(f'media id: {media_id}, zone id: {zone_id}')

    # banner 정보 가지고옴

    # markup 정보 뱉음
    pass

def generate_messages():
    topic = "info"
    sender = MessageProducer(broker, topic)
    user_id = 1
    while True:
        message = {f"user_{user_id}": {"click": 1, "impression": 1}}
        print(message)
        sender.send_message(message)
        user_id += 1
        time.sleep(5)  # 5초마다 전송


if __name__ == "__main__":
    generate_messages()