from fastapi import FastAPI, Response, Depends
import pathlib
import json
from typing import Union, List
from models import ItemPydanticModel
from database import ItemSQLModel, engine
from sqlmodel import Session, select


app = FastAPI()

ITEMS_LIST = []

@app.on_event("startup")
async def startup_event():
    print("Jest fajnie może zadziałam")

def get_session():
    with Session(engine) as session:
        yield session

#Strona Powitalna
@app.get('/')
def hello_world():
    return 'Witaj na stronie z zabytkami. Możesz sobie poklikać i bedzie wpyte.'

#Wyplucie wszystkim rekordów z bazy
@app.get('/items/', response_model=List[ItemPydanticModel])
def get_items(session: Session = Depends(get_session)):
    stmt = select(ItemSQLModel)
    result = session.exec(stmt).all()
    return result

#Wydobycie jednego itemu z bazy
@app.get('/items/{item_id}', response_model=Union[ItemPydanticModel, str])
def get_item_by_id(item_id: int, respone: Response, session: Session = Depends(get_session)):
    item = session.get(ItemSQLModel, item_id)
    if item is None:
        Response.status_code = 404
        return "Item not found"
    return item 

#Dodaj nowy zabytek
@app.post('/items/', response_model=ItemPydanticModel, status_code=201)
def create_item(item: ItemSQLModel, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

#Update zabytku
@app.put('/item/{item_id}', response_model=Union[ItemPydanticModel, str])
def update_item(item_id: int, updated_item: ItemPydanticModel, respone: Response, session: Session = Depends(get_session) ):
    
    item = session.get(ItemSQLModel, item_id)

    if item is None:
        Response.status_code = 404
        return "Item not found"
    
    item_dict = updated_item.model_dump(exclude_unset = True)

    for key, val in item_dict.items():
        setattr(item, key, val)
    
    session.add(item)
    session.commit()
    session.refresh(item)

    return item 

#Usuń zabytek
@app.delete('/item/{item_id}')
def delete_item(item_id: int, respone: Response, session: Session = Depends(get_session)):
    item = session.get(ItemSQLModel, item_id)

    if item is None:
        Response.status_code = 404
        return "Item not found"

    session.delete(item)
    session.commit()
    return Response(status_code=200 )

