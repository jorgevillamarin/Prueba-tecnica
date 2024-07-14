from fastapi import APIRouter, Depends, HTTPException
from models.Models import TransactionResponse
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import date
from config.database import get_db, Base, engine, sessionmaker
from Router.funtion.crud import get_financial_summary, get_transactions_by_category, get_transactions_by_date


# Creacion las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Configura la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


funtion=APIRouter()



@funtion.get("/financial_summary/", response_model=Dict[str, float])
def get_financial_summary_for_period(start_date: date, end_date: date, db: Session = Depends(get_db)):
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date")
    return get_financial_summary(db, start_date, end_date)

@funtion.get("/transactions/by_category/", response_model=List[TransactionResponse])
def read_transactions_by_category( category: str, db: Session = Depends(get_db)
):
    if not category:
        raise HTTPException(status_code=400, detail="Category parameter is required")
    
    transactions = get_transactions_by_category(db, category=category)
    
    if not transactions:
        raise HTTPException(status_code=404, detail=f"No transactions found with category '{category}'")
    
    return transactions

@funtion.get("/transactions/by-date/", response_model=List[TransactionResponse])
def read_transactions_by_date(
    fecha: date,
    db: Session = Depends(get_db)
):
    transactions = get_transactions_by_date(db, fecha=fecha)
    
    if not transactions:
        raise HTTPException(status_code=404, detail=f"No transactions found for date '{fecha}'")
    return transactions


