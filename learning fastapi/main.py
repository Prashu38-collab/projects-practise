from fastapi import FastAPI

app=FastAPI()

@app.get("/") #path(/):simple homepage
def home():
    return {"message":"hello without virtual environment"}