from fastapi import FastAPI, HTTPException, Request, Form, Depends, UploadFile, File
from starlette.responses import Response, RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import json
import shutil
import os
from json import JSONEncoder

from app.db.models import *
from app.db import models, schema, crud

from .db.database import SessionLocal, engine

import string, random, pathlib



models.Base.metadata.create_all(bind=engine)


tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Influencers",
        "description": "Operations with influencers.",
    },
    {
        "name": "Organizations",
        "description": "Operations with organizations.",
    },
    {
        "name": "Campaigns",
        "description": "Operations with campaigns.",
    },
]


app = FastAPI(
    title="Influencer Marketing Platform API",
    openapi_tags=tags_metadata
)

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# @app.get("/")
# def root():
#     return {"message": "Fast API in Python"}

# @app.get("/db_check")
# async def db_check(request: Request, id: int, db: Session = Depends(get_database_session)):
#     print(db)
#     return JSONResponse(status_code=200, content={
#         "status_code": 200,
#         "message": "success",
#         # "movie": newMovie
#     })


# @app.get("/user/{id}")
# def read_user_by_id(request: Request, id: int, db: Session = Depends(get_database_session)):
#     record = db.query(User).filter(User.id==id).first()
#     return JSONResponse(status_code=200, content={
#         "status_code": 200,
#         "message": "success",
#         "user": jsonable_encoder(record)
#     })
    
@app.get("/user/", response_model=schema.UserReturn, tags=["Users"])
def get_user_by_name(request: Request, id: int, db: Session = Depends(get_database_session)):
    db_user = crud.get_user_by_id(db=db, id=id)
    return db_user
    
@app.post("/user/", response_model=schema.User, tags=["Users"])
def create_user(request: Request, user: schema.UserCreate, db: Session = Depends(get_database_session)):
    db_user = crud.get_user_by_name(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, item=user)

@app.post("/influencer/", response_model=schema.Influencer, tags=["Influencers"])
def create_influencer(request: Request, user_id: int, influencer_item: schema.InfluencerCreate, db: Session = Depends(get_database_session)):
    inf = crud.create_influencer(db=db, item=influencer_item)
    db_user = crud.update_user(db=db, user_id=user_id, inf_id=inf.id)
    return inf

@app.get("/influencer/", response_model=schema.Influencer, tags=["Influencers"])
def get_influencer_by_id(inf_id:int, db: Session = Depends(get_database_session)):
    return crud.get_influencer(db=db, inf_id=inf_id)

@app.get("/influencer/list", response_model=List[schema.Influencer], tags=["Influencers"])
def get_influencer_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    return crud.get_influencer_list(db=db)

@app.get("/social_accounts/", response_model=List[schema.SocialAccount], tags=["Influencers"])
def get_social_accounts(inf_id:int, db: Session = Depends(get_database_session)):
    accounts = crud.get_user_social_accounts(db, inf_id==inf_id)
    return accounts

@app.post("/social_accounts/", response_model=schema.SocialAccount, tags=["Influencers"])
def create_social_account(request: Request, inf_id:int, social_account: schema.SocialAccountCreate, db: Session = Depends(get_database_session)):
    db_sa = crud.get_user_social_accounts_by_type(db, inf_id=inf_id, type=social_account.account_type)
    if db_sa:
        raise HTTPException(status_code=400, detail="This type of social account already registered on user")
    return crud.create_social_account(db=db, item=social_account, inf_id=inf_id)

    
@app.post("/organization/", response_model=schema.Organization, tags=["Organizations"])
def create_org(request: Request, user_id: int, org: schema.OrganizationCreate, db: Session = Depends(get_database_session)):
    db_org = crud.get_org_by_name(db, name=org.name)
    if db_org:
        raise HTTPException(status_code=400, detail="Org already registered")
    db_org = crud.create_orgs(db=db, item=org)
    crud.update_user(db=db, user_id=user_id, org_id=db_org.id)
    return db_org

@app.get("/organizations/", response_model=List[schema.Organization], tags=["Organizations"])
def read_orgs(skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    orgs = crud.get_orgs(db, skip=skip, limit=limit)
    return orgs


@app.post("/campaign/create", response_model=schema.Campaign, tags=["Campaigns"])
def create_campaign(request: Request, org_id:int, campaign: schema.CampaignCreate, db: Session = Depends(get_database_session)):
    db_campaign = crud.get_campaign_by_name(db, name=campaign.title, org_id=org_id)
    if db_campaign:
        raise HTTPException(status_code=400, detail="Campaign with this name already registered")
    return crud.create_campaign(db=db, item=campaign, org_id=org_id)

@app.post("/campaign/update", response_model=schema.Campaign, tags=["Campaigns"])
def update_campaign(request: Request, campaign_id:int, campaign: schema.CampaignCreate, db: Session = Depends(get_database_session)):
    return crud.update_campaign(db=db, item=campaign, campaign_id=campaign_id)

@app.get("/campaigns/", response_model=List[schema.Campaign], tags=["Campaigns"])
def read_campaigns(org_id:int, skip: int = 0, limit: int = 100, db: Session = Depends(get_database_session)):
    campaigns = crud.get_campaigns_by_org_id(db, org_id==org_id, skip=skip, limit=limit)
    return campaigns


@app.post("/upload/")
async def create_upload_file(request: Request, file: UploadFile = File(None)):
    file.file.seek(0, 2)
    file_size = file.file.tell()

    # move the cursor back to the beginning
    await file.seek(0)

    if file_size > 2 * 1024 * 1024:
        # more than 2 MB
        raise HTTPException(status_code=400, detail="File too large")

    # check the content type (MIME type)
    content_type = file.content_type
    if content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # do something with the valid file
    upload_dir = os.path.join(os.getcwd(), "./static")
    # Create the upload directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # get the destination path
    file_extension = pathlib.Path(file.filename).suffix

    filename = get_randomname_string() + file_extension
    dest = os.path.join(upload_dir, filename)
    print(dest)

    # copy the file contents
    with open(dest, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    url = str(request.url).replace("upload", "static")
    return {"file_url": url + filename}


def get_randomname_string():
    # choose from all lowercase letter
    letters = string.ascii_lowercase + string.digits
    result_str = ''.join(random.choice(letters) for i in range(30))
    return result_str