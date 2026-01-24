import os
import uuid

from sqlalchemy import Column, String, Float, Boolean, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@db:5432/aura_db")

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    base_price = Column(Float, nullable=False)
    floor_price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    meta = Column(JSONB, default={})
    embedding = Column(Vector(1024))


def init_db():
    Base.metadata.create_all(bind=engine)
