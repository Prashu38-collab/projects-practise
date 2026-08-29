from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

app=FastAPI()
# Allow requests from the Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connectiion and setup
DATABASE_URL = "sqlite:///study_activity.db"
engine= create_engine(DATABASE_URL, echo=True)

# creating session - it is used to interact with the database
Session=sessionmaker(bind=engine)
Base=declarative_base()
#  stdy Activity table model usinfg orm -
class StudyActivity(Base):
    __tablename__ = "study_activities"
    id=Column(Integer,primary_key=True)
    title=Column(String)
    url=Column(String)
    duration=Column(Float)
# Create the table in the database
Base.metadata.create_all(engine)

# post function - that recives the json file from chrome and add to activity which is a dict
@app.post("/activity")
def receive_activity(activity: dict): #this is a typehint
    db_session = Session()
    study_activity = StudyActivity(
        title=activity.get("title"),
        url=activity.get("url"),
        duration=activity.get("duration")
    )
    db_session.add(study_activity)
    db_session.commit()
    db_session.close()
    print("Received activity:")
    print(activity)

    return {"status": "received"}
# get activities from what is stored in list activities to verify what is present.
@app.get("/activities")
def get_activities():
    db_session = Session()
    activities = db_session.query(StudyActivity).all()
    db_session.close()
    return activities