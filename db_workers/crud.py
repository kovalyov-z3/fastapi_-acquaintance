from .database import User, Url
from sqlalchemy.orm import Session
import string
import random


__all__ = ["save_user", "save_url", "select_url", "select_short_url", "select_user","select_password", "select_my_url", "select_user_id"]

def save_user(db:Session, email, hashed_password):
    db_user = User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()

def save_url(db:Session, long_url, user_id):
    db_url = Url(long_url=long_url, short_url=generate_short_url(), user_id=user_id)
    db.add(db_url)
    db.commit()

def select_url(db:Session, short_url):
    return db.query(Url.long_url).filter(Url.short_url==short_url).first()

def select_short_url(db:Session, long_url):
    return db.query(Url.short_url).filter(Url.long_url==long_url).first()

def select_user(db:Session, email):
    return db.query(User.is_active).filter(User.email == email).first()

def select_user_id(db:Session, email):
    return db.query(User.user_id).filter(User.email == email).first()["user_id"]

def select_password(db:Session, email):
        return db.query(User.hashed_password).filter(User.email == email).first()["hashed_password"]

def select_my_url(db:Session, user_id):
    short_part = db.query(Url.short_url).filter(Url.user_id == user_id).all()
    long_part = db.query(Url.long_url).filter(Url.user_id == user_id).all()
    return dict(zip([i["long_url"] for i in long_part], ["http://127.0.0.1:8000/"+i["short_url"] for i in short_part]))

def generate_short_url():
    characters = string.ascii_letters + string.digits
    stop = random.randint(3, 10)
    return ''.join(random.choice(characters) for i in range(1, stop))

if __name__ == "__main__":
    print(generate_short_url())
