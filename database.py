from typing import Optional
from sqlmodel import Field, SQLModel, create_engine

DATABASE = 'db.sqlite3'
engine = create_engine(f'sqlite:///{DATABASE}', echo=True)

class ItemModel(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    localization: str
    date: Optional[str] = Field(default=None)
    image: str
    ticket_price: Optional[float] = Field(default=None) 

def create_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == '__main__':
    create_tables()