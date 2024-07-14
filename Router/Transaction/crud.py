from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException
from models.Models import Transaction,TransactionCreate,TransactionBase

def create_transaction(db: Session, transaction_data: TransactionCreate):
    db_transaction = Transaction(
        type=transaction_data.type,
        amount=transaction_data.amount,
        category=transaction_data.category,
        fecha=transaction_data.fecha,
        description=transaction_data.description
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_all_transactions(db: Session, offset: int = 0, limit: int = 20) -> List[Transaction]:
    transactions = db.query(Transaction).offset(offset).limit(limit).all()
    return transactions
def get_total_transactions_count(db: Session) -> int:
    count = db.query(Transaction).count()
    return count



def get_transaction_by_id(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()


def update_transaction(db: Session, id: int, update: TransactionBase):
    db_update = db.query(Transaction).filter(Transaction.id == id).first()
    if db_update is None:
        raise HTTPException(status_code=404, detail="transaccion no encontrada")
    for var, value in vars(update).items():
        setattr(db_update, var, value) if value else None
    db.commit()
    db.refresh(db_update)
    return db_update

def delete_transacion(db: Session, id: int):
    a_eliminar = db.query(Transaction).filter(Transaction.id == id).first()
    if a_eliminar:
        db.delete(a_eliminar)
        db.commit()
        return (HTTPException(status_code=200))
    return (HTTPException(status_code=404, detail="transaccion no encontrada"))

