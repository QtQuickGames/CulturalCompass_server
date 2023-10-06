from typing import Optional, List
from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlalchemy import ARRAY, String, Column
import json
import os

DATABASE = 'C:/Users/marcz/Desktop/Hackaton2023Plock/CulturalCompass_server/db.sqlite3'
engine = create_engine(f'sqlite:///{DATABASE}', echo=True)

session = Session(engine)
folder_path = 'C:\\Users\\marcz\\Desktop\\Hackaton2023Plock\\database\\relics-json'

'description', 'documents', 'date', 'fprovince', 'name', 'links', 'common_name', 'longitude', 'documents_info', 'identification', 'midi', 'latitude', 'alternate_text', 'categories', 'country_code', 'main_photo', 'photos', 'file', 'full', 'links_info', 'tags', 'file_full_width', 'street', 'descendants', 'district_name', 'url', 'events', 'author', 'entries', 'fplace', 'register_number', 'state', 'place_name', 'commune_name', 'alerts', 'body', 'mini', 'dating_of_obj', 'nid_id'

class ItemSQLModel(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nid_id: Optional[str] = Field(default = None)
    identification: Optional[str] = Field(default = None)
    common_name: Optional[str] = Field(default = None)
    description: Optional[str] = Field(default = None)
    state: Optional[str] = Field(default = None)
    register_number: Optional[str] = Field(default = None)
    dating_of_obj: Optional[str] = Field(default = None)
    street: Optional[str] = Field(default = None)
    latitude: Optional[float] = Field(default = None)
    longitude: Optional[float] = Field(default = None)
    country_code: Optional[str] = Field(default = None)
    fprovince: Optional[str] = Field(default = None)
    fplace: Optional[str] = Field(default = None)
    documents_info: Optional[str]= Field(default = None)
    links_info: Optional[str] = Field(default = None)
    main_photo: Optional[str] = Field(default = None)
    place_id: Optional[int] = Field(default = None)
    place_name: Optional[str] = Field(default = None)
    commune_name: Optional[str] = Field(default = None)
    district_name: Optional[str] = Field(default = None)
    voivodeship_name: Optional[str] = Field(default = None)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def import_data_from_json(json_file_path: str):
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        #print(data.get("nid_id"))
        # Przypisz tylko te informacje, które są dostępne w modelu Item
        
        item_data = {
            "nid_id": data.get("nid_id"),
            "identification": data.get("identification"),
            "common_name": data.get("common_name", ""),
            "description": data.get("description", ""),
            #"categories": data.get("categories", []),
            "state": data.get("state"),
            "register_number": data.get("register_number"),
            "dating_of_obj": data.get("dating_of_obj"),
            "street": data.get("street"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            #"tags": data.get("tags", []),
            "country_code": data.get("country_code"),
            "fprovince": data.get("fprovince"),
            "fplace": data.get("fplace"),
            "documents_info": data.get("documents_info"),
            "links_info": data.get("links_info"),
            "main_photo": data.get("main_photo",{}).get("file",{}).get("url"),
            #"events": data.get("events", []),
            #"entries": data.get("entries", []),
            #"links": data.get("links", []),
            #"documents": data.get("documents", []),
            #"alerts": data.get("alerts", []),
            #"photos": data.get("photos", []),
            "place_id": data.get("place_id"),
            "place_name": data.get("place_name"),
            "commune_name": data.get("commune_name"),
            "district_name": data.get("district_name"),
            "voivodeship_name": data.get("voivodeship_name")
        }
        
        # Wyciągnij tylko pierwszy element ze słownika main_photo, jeśli istnieje
        #main_photo = data.get("main_photo").get("file").get("url")
        #print(main_photo)
        #url_photo = main_photo["file"]['url']
        #print(url_photo)
        
        #item_data["main_photo"] = main_photo
        # Utwórz obiekt ItemModel i dodaj go do bazy danych

        item = ItemSQLModel(**item_data)
        with Session(engine) as session:
            session.add(item)
            session.commit()

def update_all_items(json_file_path: str):
    
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    with Session(engine) as session:
        statement = select(ItemSQLModel)
        results = session.exec(statement)
        items = results.all()
        for item in items:
            item.main_photo = data.get("main_photo",{}).get("file",{}).get("url")
            session.add(item)
            session.commit()

def get_json_files_in_folder(folder_path):
    json_files = []
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".json"):
                json_files.append(os.path.join(root, file_name))
    return json_files





    #import_data_from_json(json_file)


if __name__ == "__main__":
    json_files = get_json_files_in_folder(folder_path)  
    
    create_db_and_tables()

    for json_file in json_files:
        import_data_from_json(json_file)
        #update_all_items(json_file)
'''
    events: Optional[str] = Field(default = None) #list
    entries: Optional[str] = Field(default = None)  #list
    links: Optional[str] = Field(default = None) #list
    documents: Optional[str] = Field(default = None) #list
    alerts: Optional[str] = Field(default = None) #list
    photos: Optional[str] = Field(default = None)  #list
    tags: Optional[str] = Field(default = None) #list
    categories: Optional[str] = Field(default = None) #list
'''