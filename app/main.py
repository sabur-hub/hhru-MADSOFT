from fastapi import FastAPI
from app.database import SessionLocal, engine
from app import models, crud, services
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В реальном приложении надо указать конкретные домены потому что это cors 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API endpoints
@app.get("/memes")
def get_memes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_memes(db, skip=skip, limit=limit)

@app.get("/memes/{id}")
def get_meme(id: int, db: Session = Depends(get_db)):
    return crud.get_meme(db, id=id)

@app.post("/memes")
def create_meme(meme: schemas.MemeCreate, db: Session = Depends(get_db)):
    return crud.create_meme(db=db, meme=meme)

@app.put("/memes/{id}")
def update_meme(id: int, meme: schemas.MemeUpdate, db: Session = Depends(get_db)):
    return crud.update_meme(db=db, id=id, meme=meme)

@app.delete("/memes/{id}")
def delete_meme(id: int, db: Session = Depends(get_db)):
    return crud.delete_meme(db=db, id=id)
