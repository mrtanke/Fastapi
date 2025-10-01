from typing import Annotated

from fastapi import Body, Depends, FastAPI, HTTPException, Query
from contextlib import asynccontextmanager
from sqlmodel import Field, SQLModel, Session, create_engine, select

app = FastAPI()

# database models
class HeroBase(SQLModel): # No talbe=True -> base class with data model
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str

class HeroPublic(HeroBase):
    id: int

class HeroCreate(HeroBase):
    secret_name: str
    
class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None

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
@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

# Path function -> Read heroes (read)
@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep, 
    offset: int=0, 
    limit: Annotated[int, Query(le=100)] = 100
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

# Path function -> Read a single hero (read)
@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
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

# Path function -> Update a hero (update)
@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    hero_data = hero.model_dump(exclude_unset=True)
    session.sqlmodel_update(hero_data)
    session.commit()
    session.refresh(hero_db)

    return hero_db