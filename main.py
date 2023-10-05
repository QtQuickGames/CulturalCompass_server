from fastapi import FastAPI, Response, Depends
import pathlib
import json
from typing import Union, List
from models import Item
from database import Item, engine
from sqlmodel import Session, select


app = FastAPI()

ITEMS_LIST = []

@app.on_event("startup")
async def startup_event():
    #To są rzeczy do zainicjalizowania bazy danych gdybyśmy mieli plik typu json z opisem zabytków
    datapath = pathlib.Path() / 'data'/ 'zabytki.json'

    #Start bazy danych
    session = Session(engine)

    #stmt - czyli statement - czyli zapytanie sqlowe
    stmt = select(Item)
    
    #uruchomienie statementu na bazie
    result = session.exec(stmt).first()

    if result is None:
        with open(datapath, 'r') as f:
            items = json.load(f)
            for item in items:
                session.add(Item(**item))
        session.commit()
    session.close()

def get_session():
    with Session(engine) as session:
        yield session

@app.get('/items/', response_model=List[Item])
def get_items(session: Session = Depends(get_session)):
    stmt = select(Item)
    result = session.exec(stmt).all()
    return result

@app.get('/items/{item_id}', response_model=Union[Item, str])
def get_item_by_id(item_id: int, respone: Response, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if item is None:
        Response.status_code = 404
        return "Item not found"
    return item 


@app.post('/items/', response_model=Item, status_code=201)
def create_item(item: Item, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.put('/item/{item_id}', response_model=Union[Item, str])
def update_item(item_id: int, updated_item: Item, respone: Response, session: Session = Depends(get_session) ):
    item = session.get(Item, item_id)

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

@app.delete('/item/{item_id}')
def delete_item(item_id: int, respone: Response, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)

    if item is None:
        Response.status_code = 404
        return "Item not found"

    session.delete(item)
    session.commit()
    return Response(status_code=200)

