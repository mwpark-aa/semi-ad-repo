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
