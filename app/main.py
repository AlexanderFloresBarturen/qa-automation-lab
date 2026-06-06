from fastapi import FastAPI

from app.routes import users
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

@app.get("/")
def root():
    return {"message": "QA Automation Lab API"}