from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

# Define la tabla users
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    email = Column(String)

    age = Column(Integer)
    
    is_active = Column(Boolean, default=True)