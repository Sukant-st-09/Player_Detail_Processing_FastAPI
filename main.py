from fastapi import FastAPI,Depends
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
    if db_player:
        return db_player
    return "No Such id"

@app.get("/Player/sport/{Sport}")
def get_players_by_sport(Sport : str,db: Session = Depends(get_db)):
    db_player = db.query(database_model.Players).filter(func.lower(database_model.Players.Sport) == Sport.lower()).all()
    return db_player

@app.post("/Player")
def add_player(player:Players,db: Session = Depends(get_db)):
    db_player = db.query(database_model.Players).filter(database_model.Players.id == player.id).first()
    if db_player is None:
        db.add(database_model.Players(**player.model_dump()))
        db.commit()
        return "Player Added Successfully"
    else:
        return "Player Id Already Exist"

@app.put("/Player")
def update_player(id:int,player:PlayerUpdate,db: Session = Depends(get_db)):
    db_player = db.query(database_model.Players).filter(database_model.Players.id == id).first()
    if db_player:
        update_player = player.model_dump(exclude_unset=True)
        for key,value in update_player.items():
            setattr(db_player,key,value)
        db.commit()
        return "Update Successful"
    
    else:
        return "No Player Id Found"
    
@app.delete("/Player")
def delete_player(id:int,db: Session = Depends(get_db)):
    db_player = db.query(database_model.Players).filter(database_model.Players.id == id).first()
    if db_player:
        db.delete(db_player)
        db.commit()
        return "Player Details Deleted Successfully"
    else:
        return "Id Not Found"