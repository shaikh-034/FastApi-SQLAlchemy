from fastapi import FastAPI, Body, Depends
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        
app = FastAPI()

fakeDatabase = {
    1:{'task':'Clean Room'},
    2:{'task':'Clean Office'},
    3:{'task':'Clean Garden'}
}

@app.get("/")
def getItems(session : Session = Depends(get_session)):
    items = session.query(models.Item).all()
    # return ['Item 1', 'Item 2', 'Item 3']
    # return fakeDatabase
    return items

@app.get("/{id}")
def getItem(id:int, session : Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item

## Option 01
# @app.post("/")
# def addItem(task:str):
#     newId = len(fakeDatabase.keys()) + 1
#     fakeDatabase[newId] = {'task':task}
#     return fakeDatabase

## Option 02
# @app.post("/")
# def addItem(item:schemas.Item):
#     newId = len(fakeDatabase.keys()) + 1
#     fakeDatabase[newId] = {'task':item.task}
#     return fakeDatabase
@app.post("/")
def addItem(item:schemas.Item, session : Session = Depends(get_session)):
    item = models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


## Option 03
# @app.post("/")
# def addItem(body=Body()):
#     newId = len(fakeDatabase.keys()) + 1
#     fakeDatabase[newId] = {'task':body['task']}
#     return fakeDatabase

# @app.put("/{id}")
# def updateItem(id:int, item:schemas.Item):
#     fakeDatabase[id]['task'] = item.task
#     return fakeDatabase

@app.put("/")
def addItem(id:int, item:schemas.Item, session : Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject

@app.delete("/{id}")   
def deleteItem(id:int, session : Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'item was deleted'