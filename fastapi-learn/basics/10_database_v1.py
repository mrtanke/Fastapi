from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from contextlib import asynccontextmanager
from sqlmodel import Field, SQLModel, Session, create_engine, select

app = FastAPI()

# a database model
class Hero(SQLModel, table=True): # talbe=True -> table model, otherwise data model
    id: int | None = Field(default=None, primary_key=True) # Field: add more metadata
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str

# a SQLModel engine -> holds the connection to the database
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Function -> create the tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Function -> create a session dependency -> open a new session for each request
#   use engine to communicate with the database.
def get_session():
    with Session(engine) as session:
        yield session
SessionDep = Annotated[Session, Depends(get_session)]

# Startup Funtion -> Create database tables on Startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
app = FastAPI(lifespan=lifespan)

# Path function -> Create a Hero (insert/update/delete)
@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep):
    session.add(hero)
    session.commit()
    session.refresh(hero) # resynchorize the real data in the database, and assign it to python
    return hero

# Path function -> Read heroes (read)
@app.get("/heroes/")
def read_heroes(
    session: SessionDep, 
    offset: int=0, 
    limit: Annotated[int, Query(le=100)] = 100
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

# Path function -> Read a single hero (read)
@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id) # Param: Hero -> indicates the search table
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

# Path function -> Delete a hero (delete)
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    session.delete(hero)
    session.commit()
    return {"ok": True}