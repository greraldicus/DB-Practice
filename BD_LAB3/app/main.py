from typing import List

from app import models
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, get_db, SessionLocal
from .models import Regions, People
from . import schemas, models

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from .repo import RegionRepository, PeopleRepository

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

'''
@app.get('/regions/')
def get_regions(db: Session = Depends(get_db)):
    regions = db.query(models.Regions).all()
    return {"regions": regions}


@app.get('/people/')
def get_people(db: Session = Depends(get_db)):
    people = db.query(models.Peoples).all()
    return {"people": people}


@app.get('/regions/{regionId}', status_code=200)
def get_persons_from_region(region_id: int, db: Session = Depends(get_db)):
    people = db.query(models.Peoples).filter(models.Peoples.region_id == region_id)
    return {"people": [person.name for person in people]}


@app.get('/people_from_regions/', status_code=200)
def get_all_persons_from_regions(db: Session = Depends(get_db)):
    people = db.query(models.Peoples).filter(models.Peoples.region_id != None)
    return {"people": [person.name for person in people]}


@app.post("/people/", status_code=201)
def create_person(person: schemas.PeoplesBase, db: Session = Depends(get_db)):
    if person.region_id is not None:
        region = db.query(models.Regions).filter(models.Regions.id == person.region_id).first()
        if region is None:
            raise HTTPException(status_code=404, detail="Регион не найден")
    person = models.Peoples(**person.dict())
    db.add(person)
    db.commit()
    db.refresh(person)
    return {"status": "success", "person": person}


@app.patch("/people/{region_id}", status_code=204)
def update_person_region(person_id: int, region_id: int, db: Session = Depends(get_db)):
    person = db.query(models.Peoples).filter(models.Peoples.id == person_id).first()
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
    person = db.query(models.Peoples).filter(models.Peoples.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=404, detail="Человек не найден")
    person.name = person_name
    db.commit()
    db.refresh(person)
    return {"status": "success", "person": person}


@app.delete('/people/{personId}')
def delete_person(person_id: str, db: Session = Depends(get_db)):
    person = db.query(models.Peoples).filter(models.Peoples.id == person_id).first()
    if not person:
        raise HTTPException(status_code=404, detail=f'Человек c id {person_id} не найден')
    db.delete(person)
    db.commit()
    return Response(status_code=404)


@app.put("/people/delete/", status_code=202)
def delete_person_from_region(person_id: int, db: Session = Depends(get_db)):
    person = db.query(models.Peoples).filter(models.Peoples.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=404, detail="Человек не найден")

    person.region_id = None
    db.commit()
    db.refresh(person)
    return {"status": "success", "person": person}
'''

# Создание экземпляров репозиториев
people_repo = PeopleRepository(session)
region_repo = RegionRepository(session)


@app.get('/people/all')
def get_all_people():
    all_people = people_repo.get_all_people()
    return all_people

@app.get('/regions/all')
def get_all_regions():
    all_regions = region_repo.get_all_regions()
    return all_regions

@app.get('/people/{region_id}')
def get_all_people_by_region_id(reg_id:int):
    peoples = people_repo.get_people_by_region_id(reg_id)
    if peoples:
        return peoples
    else:
        return {'error': 'People not found'}

@app.get('/people')
def get_all_people_by_region():
    peoples = people_repo.get_people_by_region()
    if peoples:
        return peoples
    else:
        return {'error': 'People not found'}


@app.post('/people')
def create_people(surname: str = None, name: str = None, patronymic: str = None, sex: str = None, region_id: int = None):
    new_people = people_repo.create_people(surname, name, patronymic, sex, region_id)
    if new_people:
        return new_people
    else:
        return {'error': 'Region not found'}


@app.put('/people/{id}/{region_id}')
def update_people_region(id: int, region_id: int):
    updated_people = people_repo.update_people_region(id, region_id)
    if updated_people == 0:
        return {'error': 'People not found'}

    if updated_people != 1:
        return updated_people
    else:
        return {'error': 'Region not found'}




@app.put('/people/{id}/{surname}/{name}/{patronymic}')
def update_people_s_n_p(id: int, surname: str, name: str, patronymic: str):
    updated_people = people_repo.update_people_s_n_p(id, surname, name, patronymic)
    if updated_people:
        return updated_people
    else:
        return {'error': 'People not found'}

@app.post('/regions')
def create_region(region_name: str):
    new_region = region_repo.create_region(region_name)
    return new_region

@app.delete('/regions/{id}/{flag}')
def delete_region(id: int,flag: bool):
    #flag = True - просто удалить регион
    if flag:
        deleted = region_repo.delete_region(id)
        if deleted:
            return {'message': 'Region deleted'}
        else:
            return {'error': 'Region not found'}
    else:
        deleted = people_repo.delete_people_by_region(id)
        delete_r = region_repo.delete_region(id)
        if deleted:
            return {'message': 'People deleted'}
        else:
            return {'error': 'People not found'}


@app.put('/regions/{id}')
def update_region(id: int, region_name: str):
    updated_region = region_repo.update_region(id, region_name)
    if updated_region:
        return updated_region
    else:
        return {'error': 'Region not found'}



@app.delete('/people/{id}')
def delete_people(id: int):
    deleted = people_repo.delete_people(id)
    if deleted:
        return {'message': 'People deleted'}
    else:
        return {'error': 'People not found'}

@app.put('/people/{id}')
def delete_people_from_region(id: int):
    updated = people_repo.update_people_delete_region(id)
    if updated:
        return {'message': 'People deleted from region'}
    else:
        return {'error': 'People not found'}



session.commit()




