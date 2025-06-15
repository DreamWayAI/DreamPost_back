from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Дозволити всі фронтенди (можна обмежити потім)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "DreamPost backend active"}

@app.post("/publish")
async def handle_publish(req: Request):
    data = await req.json()
    print(">>> Отримано:", data)
    return {"message": "✅ Прийнято"}
