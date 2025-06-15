
from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime
import openai
import os
import asyncio
import requests

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

channel_prompts = {
    "@dreamway_ai": "Згенеруй цікавий пост у стилі каналу про штучний інтелект для бізнесу та життя",
    "@dreamtech_news": "Напиши стислий і цікавий пост про останні новини у світі технологій",
    "@business_tools": "Згенеруй практичну пораду або інструмент для бізнесу у вигляді короткого поста"
}

channel_chat_ids = {
    "@dreamway_ai": "-1001234567890",
    "@dreamtech_news": "-1009876543210",
    "@business_tools": "-1001122334455"
}

class PostRequest(BaseModel):
    channel: str
    publishAt: str  # формат ISO: '2025-06-15T18:30'
    text: str = None

async def send_telegram_message(chat_id: str, text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        r = requests.post(url, json=payload)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

async def schedule_post(channel: str, text: str, publish_time: datetime):
    delay = (publish_time - datetime.now()).total_seconds()
    if delay > 0:
        await asyncio.sleep(delay)
    await send_telegram_message(channel_chat_ids[channel], text)

@app.post("/generate_post")
async def generate_post(data: PostRequest):
    prompt = channel_prompts.get(data.channel, "Згенеруй цікавий пост")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ти телеграм-бот, що публікує дописи."},
                {"role": "user", "content": prompt}
            ]
        )
        return {"text": response.choices[0].message["content"]}
    except Exception as e:
        return {"error": str(e)}

@app.post("/schedule_post")
async def schedule_and_post(data: PostRequest, background_tasks: BackgroundTasks):
    if not data.text:
        return {"error": "Text is required"}
    try:
        publish_time = datetime.fromisoformat(data.publishAt)
        background_tasks.add_task(schedule_post, data.channel, data.text, publish_time)
        return {"status": "scheduled", "publishAt": data.publishAt}
    except Exception as e:
        return {"error": str(e)}
