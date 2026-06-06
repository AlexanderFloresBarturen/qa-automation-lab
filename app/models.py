from sqlalchemy import Column, Integer, String
from app.database import Base

# Define la tabla users
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    email = Column(String, unique=True)

    age = Column(Integer)
    