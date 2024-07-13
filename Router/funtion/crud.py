from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from typing import Dict, List
from models.Models import Transaction, category_class, Category




#Bonus de funcionalidades#
def get_financial_summary(db: Session, start_date: date, end_date: date) -> Dict[str, float]:
    income = db.query(func.sum(Transaction.amount)).filter(Transaction.type == "Ingreso", Transaction.fecha >= start_date, Transaction.fecha <= end_date).scalar() or 0
    expenses = db.query(func.sum(Transaction.amount)).filter(Transaction.type == "Gasto", Transaction.fecha >= start_date, Transaction.fecha <= end_date).scalar() or 0
    net_balance = income - expenses
    return {
        "total_income": float(income),
        "total_expenses": float(expenses),
        "net_balance": float(net_balance)
    }

def get_transactions_by_category(db: Session, category: str) -> List[Transaction]:
    transactions = db.query(Transaction).filter(Transaction.category == category).all()
    return transactions

def get_transactions_by_date(db: Session, fecha: date) -> List[Transaction]:
    transactions = db.query(Transaction).filter(Transaction.fecha == fecha).all()
    return transactions