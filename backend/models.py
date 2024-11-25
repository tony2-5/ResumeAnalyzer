# backend/models.py

from sqlalchemy import Table, Column, Integer, String
from backend.database import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("email", String, unique=True, index=True),
    Column("username", String),
    Column("hashed_password", String),
)
