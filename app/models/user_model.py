from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database.connection import Base

# Define la tabla users
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    email = Column(String)

    age = Column(Integer)
    
    is_active = Column(Boolean, default=True)

    password_hash = Column(String, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)

    role = relationship("RoleModel", back_populates="users")