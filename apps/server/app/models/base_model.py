#!/usr/bin/python3
"""
Contains class BaseModel
"""

import uuid
from datetime import datetime, UTC
from sqlalchemy import func, String, DateTime
from sqlalchemy.orm import declared_attr, declarative_mixin, Mapped, mapped_column

@declarative_mixin
class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    id: Mapped[str] = mapped_column(
        String(60),
        primary_key=True,
        default=lambda:str(uuid.uuid4()),
        index=True
        )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now())

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + "s"

    def __repr__(self):
        return f"<{self.__class__.__name__}.(id={self.id})>"
