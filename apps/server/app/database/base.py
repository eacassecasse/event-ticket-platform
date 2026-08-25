#!/usr/bin/python3
"""
Contains class Base
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class from which future SQLAlchemy ORM models will be derived"""
    pass
