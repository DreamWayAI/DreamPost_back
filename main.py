from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Додати CORS (можна вказати конкретний домен фронту замість "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # або ["https://dream-post-front-v4ra.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "DreamPost GPT backend active"}

@app.post("/publish")
async def handle_publish(req: Request):
    data = await req.json()
    print(">>> Отримано запит:", data)
    return {"message": "✅ Успішно отримано!"}
