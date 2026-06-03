from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone


# Define the base class for our ORM(Object Relational Mapping) models
Base = declarative_base()


# User table to store user information
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    micro_transaction_threshold = Column(Float, default=1000.0) 
    streak_days = Column(Integer, default=0)

    transactions = relationship("TransactionRecord", back_populates="owner")
    budgets = relationship("CategoryBudget", back_populates="owner")


# TransactionRecord table to store individual transaction records
class TransactionRecord(Base):
    __tablename__ = 'transaction_records'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    vendor = Column(String, index = True)
    category = Column(String, index = True, nullable=False)
    is_expense = Column(Boolean, default=True, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    raw_sms = Column(String, nullable=False)

    owner = relationship("User", back_populates="transactions") #User owns the transactions


# Budget table to store user budgets for different categories
class CategoryBudget(Base):
    __tablename__ = 'category_budgets'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category = Column(String, index=True, nullable=False)
    monthly_budget = Column(Float, nullable=False)
    current_spent = Column(Float, default=0.0)
    month_year = Column(String, index=True, nullable=False) # Format: MM-YYYY

    owner = relationship("User", back_populates="budgets") #User owns the budgets