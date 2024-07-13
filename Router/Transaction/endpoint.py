from fastapi import APIRouter, Depends, HTTPException, Request
from models.Models import TransactionCreate, TransactionResponse, TransactionUpdate, PaginatedResponse
from sqlalchemy.orm import Session
from typing import List, Dict
from config.database import get_db, Base, engine, sessionmaker
from Router.Transaction.crud import create_transaction,get_total_transactions_count,get_all_transactions,get_transaction_by_id, update_transaction, delete_transacion


# Creacion las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Configura la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


endpoint=APIRouter()


@endpoint.post("/transactions/", response_model=TransactionCreate)
def create_new_transaction(transaction_data: TransactionCreate, db: Session = Depends(get_db)):
    return create_transaction(db, transaction_data)


PAGE_SIZE = 20

@endpoint.get("/transactions",response_model=PaginatedResponse)
async def read_transactions(request: Request, db: Session = Depends(get_db)):
    # Calculo de la pagina anterior basado en la ruta solicitada
    current_page = request.query_params.get('page', 1)
    try:
        current_page = int(current_page)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid page parameter")
    
    if current_page < 1:
        current_page = 1

    offset = (current_page - 1) * PAGE_SIZE

    transactions = get_all_transactions(db, offset=offset, limit=PAGE_SIZE)
    total_count = get_total_transactions_count(db)
    
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    
    next_page = f"/transactions?page={current_page + 1}" if offset + PAGE_SIZE < total_count else None
    previous_page = f"/transactions?page={current_page - 1}" if current_page > 1 else None

    result = PaginatedResponse(
        transactions=[TransactionResponse.from_orm(transaction) for transaction in transactions],
        total_count=total_count,
        page_size=PAGE_SIZE,
        next_page=next_page,
        previous_page=previous_page
    )
    
    return result

@endpoint.get("/transactions/{transaction_id}", response_model=TransactionCreate)
def read_transaction_id(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = get_transaction_by_id(db, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404)
    return HTTPException(status_code=200)

@endpoint.put("/transactions/{id}")
def update_cliente(id: int, update: TransactionUpdate, db: Session = Depends(get_db)):
    return update_transaction(db, id, update)

@endpoint.delete("/transactions/{id}")
async def delete_obj(id: int, db: Session = Depends(get_db)):
    return delete_transacion(db, id)

 

