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

@app.get("/users/{user_id}")
def get_users(user_id:int):
    return {"Users":user_id}

# url ma kunai dynamic value change garnu paryo vane path parameters