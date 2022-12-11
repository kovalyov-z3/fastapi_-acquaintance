from fastapi import APIRouter, Request, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse, RedirectResponse
import hashlib
import os

from pydantic import BaseModel
from db_workers import crud
router = APIRouter()
#Seems that this sheet is working add migrations with yoyo
class Loginer(BaseModel):
    email: str
    hashed_password: str
    class Config:
        schema_extra = {
            "example": {
                "login": "Abdulazeez Abdulazeez Adeshina",
                "password": "weakpassword"
            }
        }
class Main(BaseModel):
    long_url: str
    class Config:
        schema_extra = {
            "example": {
                "long_url": "https://vk.com"
            }
        }


def get_db(request:Request):
    return request.state.db

@router.get("/all_links")
def show_all(request:Request, db:Session = Depends(get_db)):
    if request.session.get("logged_in"):
        return crud.select_my_url(db=db, user_id=request.session["user_id"])




@router.post("/")
def index_post(main:Main, request:Request, db: Session = Depends(get_db)):
    if request.session.get("logged_in"):
        crud.save_url(db, long_url=main.long_url, user_id=request.session["user_id"])
        
        answer = "http://127.0.0.1:8000/" + str(crud.select_short_url(db, long_url=main.long_url)["short_url"])
        return {"message": answer}
    else:
        return {"message":"Hold on, bro, u need to be logged in!"}

@router.get("/")
def index_get(request:Request):
    if request.session.get("logged_in"):
        return FileResponse("public/main.html")
    else:
        return RedirectResponse("/login/index")

@router.get("/{short_url}")
def index(short_url, request:Request, db: Session = Depends(get_db)):
    

    if request.session.get("logged_in") and short_url == "":
        return "Welcome on board, homie!"

    if request.session.get("logged_in"):
        try:
            return RedirectResponse(str(crud.select_url(db, short_url=short_url)["long_url"]))
        except:
            return {"Error": "Hold on, bro your link is invalid!"}
    
@router.get("/login/index")
def login():
    return FileResponse("public/index.html")

@router.post("/login/index")
def login_handler(loginer:Loginer, request:Request, db: Session = Depends(get_db)):
    print(loginer.email)
    if (crud.select_user(db, loginer.email) is not None):
        key = hashlib.pbkdf2_hmac(
    'sha256', # Используемый алгоритм хеширования
    str(loginer.hashed_password).encode('utf-8'),salt="kek".encode("utf-8"), iterations=1000)
        if key == crud.select_password(db=db, email=loginer.email):
            request.session["logged_in"] = True
            request.session["user_id"] = crud.select_user_id(db=db, email=loginer.email)  
            return {"message": "You were sucessfully logged in!"}
        else:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    else:
        key = hashlib.pbkdf2_hmac(
    'sha256', # Используемый алгоритм хеширования
    str(loginer.hashed_password).encode('utf-8'), "kek".encode("utf-8"), iterations=1000)
        crud.save_user(db, loginer.email, key)
        request.session["user_id"] = crud.select_user_id(db=db, email=loginer.email)
        return {"message": "You were signed up!"}