from typing import Optional

from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Ofensa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    evento: str = Field(index=True)
    descripcion: str

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/ofensa/")
def create_ofensa(ofensa: Ofensa):
    with Session(engine) as session:
        session.add(ofensa)
        session.commit()
        session.refresh(ofensa)
        return ofensa

@app.get("/ofensa/")
def read_ofensa():
    with Session(engine) as session:
        ofensas = session.exec(select(Ofensa)).all()
        return ofensas


@app.delete("/ofensa/{ofensa_id}")
def delete_ofensa(ofensa_id: int):
  raise HTTPException(status_code=502, detail="No Implementado")


@app.get("/ofensa/{ofensa_id}")
def read_ofensa(ofensa_id: int):
  raise HTTPException(status_code=502, detail="No Implementado")
