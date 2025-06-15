from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "DreamPost GPT backend active"}

@app.post("/publish")
async def publish(request: Request):
    data = await request.json()
    return {"status": "received", "data": data}