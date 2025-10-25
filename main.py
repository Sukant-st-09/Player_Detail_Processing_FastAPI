from fastapi import FastAPI, Depends, HTTPException
from models import Players,PlayerUpdate
from database import engine,session
import database_model
from sqlalchemy import func
from sqlalchemy.orm import Session

app = FastAPI()

database_model.Base.metadata.create_all(bind = engine )

@app.get("/")
def welcome():
    return "Hello, Welcome to The Player Details Portal"

players = [
    Players(id = 107 , Player_Name = "Sukant" , Age = 21 ,Gender = "Male" , Sport = "Kabbadi")
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_model.Players).count()
    if count == 0: 
        for i in players:
            db.add(database_model.Players(**i.model_dump()))
        db.commit()

init_db()

@app.get("/Players")
def all_players(db: Session = Depends(get_db)):
    db_players = db.query(database_model.Players).all()
    return db_players

@app.get("/Player/{id}")
def get_one_player(id: int,db: Session = Depends(get_db)):
    db_player = db.query(database_model.Players).filter(database_model.Players.id == id).first()
    if not db_player:
        raise HTTPException(status_code=404, detail=f"Player with id {id} not found")
    return db_player

@app.get("/Player/sport/{Sport}")
def get_players_by_sport(Sport : str,db: Session = Depends(get_db)):
    db_player = db.query(database_model.Players).filter(func.lower(database_model.Players.Sport) == Sport.lower()).all()
    if not db_player:
        raise HTTPException(status_code=404, detail=f"Player with sport {Sport} not found")
    return db_player

@app.post("/Player")
def add_player(player:Players,db: Session = Depends(get_db)):
    db_player = db.query(database_model.Players).filter(database_model.Players.id == player.id).first()
    if db_player:
        raise HTTPException(status_code=409, detail=f"Player with id {player.id} already exists")
    db.add(database_model.Players(**player.model_dump()))
    db.commit()
    return {"status": "success", "message": "Player added successfully"}

@app.put("/Player")
def update_player(id:int,player:PlayerUpdate,db: Session = Depends(get_db)):
    db_player = db.query(database_model.Players).filter(database_model.Players.id == id).first()
    if not db_player:
        raise HTTPException(status_code=404, detail=f"Player with id {id} not found")
    
    update_player = player.model_dump(exclude_unset=True)
    for key,value in update_player.items():
        setattr(db_player,key,value)
    db.commit()
    return {"status": "success", "message": "Player updated successfully"}
    
@app.delete("/Player")
def delete_player(id:int,db: Session = Depends(get_db)):
    db_player = db.query(database_model.Players).filter(database_model.Players.id == id).first()
    if not db_player:
        raise HTTPException(status_code=404, detail=f"Player with id {id} not found")
    
    db.delete(db_player)
    db.commit()
    return {"status": "success", "message": "Player deleted successfully"}