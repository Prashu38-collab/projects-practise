from fastapi import FastAPI

app=FastAPI()

# home route
@app.get("/") #path(/):simple homepage
def home():
    return {"message":"Hello! welcome,learning fast api"}
# about route 
@app.get("/about")
def about():
    return {"message":"This is about page"}

@app.get("/users")
def users():
    return {"Users":["Prashamsa","kritika","paru"]}