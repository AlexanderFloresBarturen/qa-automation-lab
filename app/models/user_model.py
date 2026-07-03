from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base

if TYPE_CHECKING:
    from app.models.role_model import RoleModel
    from app.models.token_model import PasswordResetTokenModel


# Define la tabla users
class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String, nullable=False)

    email: Mapped[str] = mapped_column(String, nullable=False)

    age: Mapped[int] = mapped_column(nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)

    failed_login_attempts: Mapped[int] = mapped_column(nullable=False, default=0)

    locked_until: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    role: Mapped["RoleModel"] = relationship(back_populates="users")
    password_reset_tokens: Mapped["PasswordResetTokenModel"] = relationship(back_populates="user")
