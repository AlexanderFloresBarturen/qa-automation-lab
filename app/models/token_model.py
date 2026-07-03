from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.connection import Base


class PasswordResetTokenModel(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    token = Column(String, nullable=False, unique=True)

    used = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, nullable=False)

    expires_at = Column(DateTime, nullable=False)

    user = relationship("UserModel", back_populates="password_reset_tokens")
