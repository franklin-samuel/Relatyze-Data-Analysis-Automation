from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, DATABASE_URL
from sqlalchemy import text

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/diagnostico-db")
def diagnostico_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        status = "conectado"
    except Exception as e:
        status = f"erro: {str(e)}"

    return {
        "status_banco": status,
        "database_url": DATABASE_URL
    }
