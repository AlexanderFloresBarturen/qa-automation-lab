from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, profile, test, users

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(test.router)


@app.get("/")
def root():
    return {"message": "QA Automation Lab API"}
