from sqlalchemy.orm import Session
from app import models, schemas

def get_memes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Meme).offset(skip).limit(limit).all()

def get_meme(db: Session, id: int):
    return db.query(models.Meme).filter(models.Meme.id == id).first()

def create_meme(db: Session, meme: schemas.MemeCreate):
    db_meme = models.Meme(text=meme.text, image_path=meme.image_path)
    db.add(db_meme)
    db.commit()
    db.refresh(db_meme)
    return db_meme

def update_meme(db: Session, id: int, meme: schemas.MemeUpdate):
    db_meme = db.query(models.Meme).filter(models.Meme.id == id).first()
    if db_meme:
        db_meme.text = meme.text
        db.commit()
        db.refresh(db_meme)
    return db_meme

def delete_meme(db: Session, id: int):
    db_meme = db.query(models.Meme).filter(models.Meme.id == id).first()
    if db_meme:
        db.delete(db_meme)
        db.commit()
    return db_meme
