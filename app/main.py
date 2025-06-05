from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Blackjack Advisor API is alive!"}


