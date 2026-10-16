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
@app.get("/college")

# optional parameters: def get_college(college: str = None): this format is removed and is not available for 3.10+
# optional paramters
def get_college(college:str|None =None): 
    return {"college":college}

# default values

@app.get("/products")
def get_products(limit: int=10):
    return {"limit":limit}

# multiple query paramaters

@app.get("/items")
def get_items(name:str|None=None,price:int=0):
    return {
        "name":name,
        "price":price
    }

    
