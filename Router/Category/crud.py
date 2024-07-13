from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import func
from datetime import date
from typing import Dict, List
from models.Models import  category_class, Category




def create_category(db: Session, category: category_class):
    db_category = Category(
        name_category=category.name_category
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_all_category(db: Session):
    return db.query(Category).all()

def delete_category(db: Session, id: int):
    category_to_delete = db.query(Category).filter(Category.id == id).first()
    if category_to_delete:
        db.delete(category_to_delete)
        db.commit()
        return category_to_delete

    return None