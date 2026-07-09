from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import users
from app.routers import auth

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/users", tags=["Users"])


@app.get("/")
def root():
    return {"message": "QA Automation Lab API"}
