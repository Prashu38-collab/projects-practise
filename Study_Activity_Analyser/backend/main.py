from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
# Allow requests from the Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
activities = []

# post function - that recives the json file from chrome and add to activity which is a dict
@app.post("/activity")
def receive_activity(activity: dict): #this is a typehint
    activities.append(activity)
    print("Received activity:")
    print(activity)

    return {"status": "received"}
# get activities from what is stored in list activities to verify what is present.
@app.get("/activities")
def get_activities():
    return activities