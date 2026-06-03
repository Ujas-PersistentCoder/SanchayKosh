from sqlalchemy.orm import Session
from app.db import db_models


def get_user_by_username(db: Session, user: str):
    """Get a user by username."""
    return db.query(db_models.User).filter(db_models.User.username == user).first()

def create_user(db: Session, user: str):
    """Creates a new user in the database."""
    new_user = db_models.User(username=user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_transaction(
        db: Session,
        user_id: int,
        amount: float,
        vencdor: str,
        category: str,
        is_expense: bool,
        raw_sms: str
):
    """Creates a new transaction record in the database for a parsed sms."""
    new_transaction = db_models.TransactionRecord(
        user_id=user_id,
        amount=amount,
        vendor=vencdor,
        category=category,
        is_expense=is_expense,
        raw_sms=raw_sms
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

def create_category_budget(
        db: Session,
        user_id: int,
        category: str,
        monthly_budget: float,
        month_year: str,
):
    """Creates a new category budget for a user."""
    new_budget = db_models.CategoryBudget(
        user_id=user_id,
        category=category,
        monthly_budget=monthly_budget,
        month_year=month_year
    )
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget