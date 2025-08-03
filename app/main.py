from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import game_ws

app = FastAPI()

app.include_router(game_ws.router)

# Serve static files (HTML client)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Blackjack Advisor API is alive!"}


