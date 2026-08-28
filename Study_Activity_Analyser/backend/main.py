from fastapi import FastAPI
app=FastAPI()

# post function - that recives the json file from chrome and add to activity which is a dict
@app.post("/activity")
def receive_activity(activity: dict): #this is a typehint
    print("Received activity:")
    print(activity)

    return {"status": "received"}
