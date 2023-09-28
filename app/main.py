from fastapi import FastAPI, HTTPException, Request, Form, Depends
from starlette.responses import Response, RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import json
from json import JSONEncoder

from app.db.models import *
from app.api import api
from app.db import models, schema, crud

from .db.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Fast API in Python"}

@app.get("/db_check")
async def db_check(request: Request, id: int, db: Session = Depends(get_database_session)):
    print(db)
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success",
        # "movie": newMovie
    })

@app.get("/user")
def read_user():
    return api.read_user()


@app.get("/user/{id}")
def read_user_by_id(request: Request, id: int, db: Session = Depends(get_database_session)):
    record = db.query(User).filter(User.id==id).first()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success",
        "user": jsonable_encoder(record)
    })
    
    
@app.post("/organization/", response_model=schema.Organization)
def create_org(request: Request, org: schema.OrganizationCreate, db: Session = Depends(get_database_session)):
    db_org = crud.get_org_by_name(db, name=org.organization_name)
    if db_org:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_orgs(db=db, item=org)

@app.get("/organizations/", response_model=List[schema.Organization])
def read_orgs(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    orgs = crud.get_orgs(db, skip=skip, limit=limit)
    return orgs


@app.post("/campaign/", response_model=schema.Campaign)
def create_campaign(request: Request, org_id:int, campaign: schema.CampaignCreate, db: Session = Depends(get_database_session)):
    db_campaign = crud.get_campaign_by_name(db, name=campaign.campaign_name, org_id=org_id)
    if db_campaign:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_campaign(db=db, item=campaign, org_id=org_id)

@app.get("/campaigns/", response_model=List[schema.Campaign])
def read_campaigns(org_id:int, skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    campaigns = crud.get_campaigns_by_org_id(db, org_id==org_id, skip=skip, limit=limit)
    return campaigns



# @app.get("/question/{position}", status_code=200)
# def read_questions(position: int, response: Response):
#     question = api.read_questions(position)

#     if not question:
#         raise HTTPException(status_code=400, detail="Error")

#     return question


# @app.get("/alternatives/{question_id}")
# def read_alternatives(question_id: int):
#     return api.read_alternatives(question_id)


# @app.post("/answer", status_code=201)
# def create_answer(payload: UserAnswer):
#     payload = payload.dict()

#     return api.create_answer(payload)


# @app.get("/result/{user_id}")
# def read_result(user_id: int):
#     return api.read_result(user_id)
