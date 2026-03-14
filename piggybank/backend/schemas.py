from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float
    note: Optional[str] = None
    date: Optional[datetime] = None

class TransactionCreate(TransactionBase):
    person_id: int

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    note: Optional[str] = None
    date: Optional[datetime] = None

class Transaction(TransactionBase):
    id: int
    person_id: int
    date: datetime

    class Config:
        from_attributes = True

class PersonBase(BaseModel):
    name: str

class PersonCreate(PersonBase):
    pass

class Person(PersonBase):
    id: int
    created_at: datetime
    balance: float = 0.0

    class Config:
        from_attributes = True

class PersonWithTransactions(Person):
    transactions: List[Transaction] = []

    class Config:
        from_attributes = True
