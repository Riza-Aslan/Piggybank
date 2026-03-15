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
    recurring_id: Optional[int] = None

    class Config:
        from_attributes = True

class RecurringTransactionBase(BaseModel):
    amount: float
    note: Optional[str] = None
    interval: str  # daily, weekly, monthly, quarterly
    start_date: datetime
    active: bool = True

class RecurringTransactionCreate(RecurringTransactionBase):
    person_id: int

class RecurringTransactionUpdate(BaseModel):
    amount: Optional[float] = None
    note: Optional[str] = None
    interval: Optional[str] = None
    active: Optional[bool] = None

class RecurringTransaction(RecurringTransactionBase):
    id: int
    person_id: int
    last_executed: Optional[datetime] = None
    next_execution: datetime
    created_at: datetime

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
