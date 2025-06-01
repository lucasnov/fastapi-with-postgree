from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import Base, engine, SessionLocal
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
import socket


app = FastAPI(title="Projeto API", version="0.1.0")

# Garante que as tabelas existam
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health-check")
def health_check(request: Request):
    return {
        "statusCode": 200,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "hostname": socket.gethostname()
    }


@app.post("/registrar", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    db_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=utils.hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login")
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not db_user or not utils.verify_password(credentials.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    token = utils.create_access_token(db_user.id)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/consultar")
def consultar(current_user: str = Depends(utils.get_current_user)):
    """
    Retorna os 10 primeiros títulos do Hacker News.
    Requer header: Authorization: Bearer <JWT>
    """
    url = "https://news.ycombinator.com"
    html = httpx.get(url, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")

    items = []
    for row in soup.select("tr.athing")[:10]:
        rank  = int(row.select_one("span.rank").get_text(strip=True).rstrip("."))
        title_tag = row.select_one(".titleline a")
        items.append({
            "rank":  rank,
            "title": title_tag.get_text(strip=True),
            "link":  title_tag["href"]
        })

    return {
        "user": current_user,
        "source": url,
        "items": items
    }
