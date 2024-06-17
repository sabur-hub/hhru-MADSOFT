from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud

def create_meme(db: Session, meme_data: schemas.MemeCreate, file: UploadFile):
    try:
        file_name = media_service.upload_image(file)
        meme_data.image_path = file_name
        return crud.create_meme(db, meme=meme_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_meme(db: Session, meme_id: int, meme_data: schemas.MemeUpdate, file: UploadFile = None):
    db_meme = crud.get_meme(db, id=meme_id)
    if not db_meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    
    if file:
        file_name = media_service.upload_image(file)
        meme_data.image_path = file_name
    
    return crud.update_meme(db, id=meme_id, meme=meme_data)
