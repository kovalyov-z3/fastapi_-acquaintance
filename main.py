from fastapi import FastAPI, Request, Depends
from fastapi.responses import Response
from auth import router
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from sqlalchemy.orm import Session
from db_workers import database
from yoyo import read_migrations
from yoyo import get_backend



app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY", max_age=None)
app.include_router(router)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = database.SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

@app.on_event("startup")
def start_func():
    print("Works!")
    backend = get_backend('sqlite:///sql_app.db')
    migrations = read_migrations('/migrations')

    with backend.lock():

        # Apply any outstanding migrations
        backend.apply_migrations(backend.to_apply(migrations))

@app.on_event("shutdown")
def stop_func():
    print("App has been stopped")
    backend = get_backend('sqlite:///sql_app.db')
    migrations = read_migrations('/migrations')

    with backend.lock():
        backend.rollback_migrations(backend.to_rollback(migrations))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)