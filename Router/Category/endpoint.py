from fastapi import APIRouter, Depends, HTTPException, Query
from models.Models import category_class
from sqlalchemy.orm import Session
from typing import List, Dict, Optional 
from datetime import date
from config.database import get_db, Base, engine, sessionmaker
from Router.Category.crud import create_category,get_all_category, delete_category


# Creacion las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Configura la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


category=APIRouter()

@category.post("/new_category/")
def create_new(category_data: category_class, db: Session = Depends(get_db)):
    return create_category(db, category_data)

@category.get("/category/")
def get_category(db: Session = Depends(get_db)):
    return get_all_category(db)

@category.delete("/category/{id}")
async def delete_ca(id: int, db: Session = Depends(get_db)):
    return delete_category(db, id)

