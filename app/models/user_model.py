from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.connection import Base


# Define la tabla users
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    email = Column(String, nullable=False)

    age = Column(Integer, nullable=False)

    is_active = Column(Boolean, nullable=False, default=True)

    password_hash = Column(String, nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)

    failed_login_attempts = Column(Integer, nullable=False, default=0)

    locked_until = Column(DateTime, nullable=True)

    role = relationship("RoleModel", back_populates="users")
    password_reset_tokens = relationship("PasswordResetTokenModel", back_populates="user")
