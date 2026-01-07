import src.core.constants as cons

from datetime import datetime
from src.clients.base import Base
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TIMESTAMP, BigInteger, Boolean, Integer, String


class Users(Base):
    __table_args__ = {"schema": "auth"}
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, server_default=cons.SQLALCHEMY_BOOL_TRUE
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, server_default=cons.SQLALCHEMY_BOOL_FALSE
    )
    role: Mapped[str] = mapped_column("role", String, server_default="'user'")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )
    last_login_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)
    failed_login_attempts: Mapped[int] = mapped_column(Integer, server_default="0")
    locked_until: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)

    logins: Mapped[list["UserLogins"]] = relationship(
        "UserLogins",
        back_populates="user",
        cascade=cons.SQLALCHEMY_DELETE_ORPHAN_CASCADE,
    )


class UserLogins(Base):
    __table_args__ = {"schema": "auth"}
    __tablename__ = "user_logins"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("auth.users.id", ondelete=cons.SQLALCHEMY_KEYWORD_CASCADE),
        nullable=False,
    )
    login_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    ip_address: Mapped[str | None] = mapped_column(String, nullable=True)

    user: Mapped["Users"] = relationship("Users", back_populates="logins")
