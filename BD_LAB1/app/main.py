from app import models
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, get_db, SessionLocal
from .models import Regions, People
from . import schemas, models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


session = SessionLocal()

region = session.query(Regions).filter(Regions.id == 1).first()
if not region:
    region1 = Regions(id=1, region_name='Мордор')
    session.add(region1)

region = session.query(Regions).filter(Regions.id == 2).first()
if not region:
    region2 = Regions(id=2, region_name='Лордерон')
    session.add(region2)

region = session.query(Regions).filter(Regions.id == 3).first()
if not region:
    region3 = Regions(id=3, region_name='Шир')
    session.add(region3)

region = session.query(Regions).filter(Regions.id == 4).first()
if not region:
    region4 = Regions(id=4, region_name='Гондор')
    session.add(region4)

session.commit()


@app.get('/regions/')
def get_regions(db: Session = Depends(get_db)):
    regions = db.query(models.Regions).all()
    return {"regions": regions}


@app.get('/people/')
def get_people(db: Session = Depends(get_db)):
    people = db.query(models.People).all()
    return {"people": people}


@app.get('/regions/{regionId}', status_code=200)
def get_people_from_region(region_id: int, db: Session = Depends(get_db)):
    people = db.query(models.People).filter(models.People.region_id == region_id)
    return {"people": [person.name for person in people]}


@app.get('/people_from_regions/', status_code=200)
def get_all_people_from_regions(db: Session = Depends(get_db)):
    people = db.query(models.People).filter(models.People.region_id != None)
    return {"people": [person.name for person in people]}


@app.post("/people/", status_code=201)
def create_person(person: schemas.PeopleBase, db: Session = Depends(get_db)):
    if person.region_id is not None:
        region = db.query(models.Regions).filter(models.Regions.id == person.region_id).first()
        if region is None:
            raise HTTPException(status_code=404, detail="Регион не найден")
    person = models.People(**person.dict())
    db.add(person)
    db.commit()
    db.refresh(person)
    return {"status": "success", "person": person}


@app.patch("/people/{region_id}", status_code=204)
def update_person_region(person_id: int, region_id: int, db: Session = Depends(get_db)):
    person = db.query(models.People).filter(models.People.id == person_id).first()
    region = db.query(models.Regions).filter(models.Regions.id == region_id).first()

    if region is None:
        raise HTTPException(status_code=404, detail="Регион не найден")
    if person is None:
        raise HTTPException(status_code=404, detail="Человек не найден")

    person.region_id = region_id
    db.commit()
    db.refresh(person)
    return {"status": "success", "person": person}


@app.patch("/people/update/{person_id}", status_code=204)
def update_person_name(person_id: int, person_name: str, db: Session = Depends(get_db)):
    person = db.query(models.People).filter(models.People.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=404, detail="Человек не найден")
    person.name = person_name
    db.commit()
    db.refresh(person)
    return {"status": "success", "person": person}


@app.delete('/people/{personId}')
def delete_person(person_id: str, db: Session = Depends(get_db)):
    person = db.query(models.People).filter(models.People.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail=f'Человек c id {person_id} не найден')
    db.delete(person)
    db.commit()
    return Response(status_code=404)


@app.put("/people/delete/", status_code=202)
def delete_person_from_region(person_id: int, db: Session = Depends(get_db)):
    person = db.query(models.People).filter(models.People.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=404, detail="Человек не найден")

    person.region_id = None
    db.commit()
    db.refresh(person)
    return {"status": "success", "person": person}

