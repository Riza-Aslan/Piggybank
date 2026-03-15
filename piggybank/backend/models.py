from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="person_rel", cascade="all, delete-orphan")
    recurring_transactions = relationship("RecurringTransaction", back_populates="person_rel", cascade="all, delete-orphan")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False) # Positive = Income/Taschengeld, Negative = Expense/Ausgabe
    note = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    recurring_id = Column(Integer, ForeignKey("recurring_transactions.id"), nullable=True, index=True)

    person_rel = relationship("Person", back_populates="transactions")
    recurring_rel = relationship("RecurringTransaction", back_populates="transactions")


class RecurringTransaction(Base):
    __tablename__ = "recurring_transactions"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    note = Column(String, nullable=True)
    interval = Column(String, nullable=False)  # daily, weekly, monthly, quarterly
    start_date = Column(DateTime, nullable=False)
    last_executed = Column(DateTime, nullable=True)
    next_execution = Column(DateTime, nullable=False, index=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    person_rel = relationship("Person", back_populates="recurring_transactions")
    transactions = relationship("Transaction", back_populates="recurring_rel")
