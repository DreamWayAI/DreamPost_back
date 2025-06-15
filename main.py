
from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import os

app = FastAPI()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")

class PostRequest(BaseModel):
    text: str
    image_url: str = None

@app.post("/publish")
def publish_post(req: PostRequest):
    if req.image_url:
        send_photo_with_caption(req.image_url, req.text)
    else:
        send_text_message(req.text)
    return {"status": "sent"}

def send_text_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

def send_photo_with_caption(image_url, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    payload = {
        "chat_id": CHANNEL_ID,
        "photo": image_url,
        "caption": caption,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)
