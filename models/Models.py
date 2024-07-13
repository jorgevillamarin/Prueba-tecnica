from sqlalchemy import Column, Integer, String, Date, Numeric
from config.database import Base
from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal
from typing import Optional, List

class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=True)
    amount = Column(Numeric(10,2), nullable=True)
    category = Column(String, nullable=True)
    fecha = Column(Date, nullable=True)
    description = Column(String, nullable=True)

class TransactionBase(BaseModel):
    type: str
    amount: Decimal = Field(..., decimal_places=2)
    category: str
    fecha: date
    description: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int

class TransactionUpdate(BaseModel):
    type: Optional[str]
    amount: Optional[Decimal] = Field(None, decimal_places=2) 
    category: str
    fecha: Optional[date]
    description: Optional[str]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class Category(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_category = Column(String)


class category_class(BaseModel):
    name_category: str
   
class PaginatedResponse(BaseModel):
    transactions: List[TransactionBase]
    total_count: int
    page_size: int
    next_page: Optional[str]
    previous_page: Optional[str]