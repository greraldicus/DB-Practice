from sqlalchemy.orm import Session
from datetime import datetime as dt

from .models import Regions, People

from sqlalchemy.orm import Session

class PeopleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_people_by_id(self, id: int):
        return self.db.query(People).filter(People.id == id).first()

    def get_people_by_region_id(self, reg_id: int):
        return self.db.query(People).filter(People.region_id == reg_id).all()

    def get_people_by_region(self):
        return self.db.query(People).filter(People.region_id.isnot(None)).all()

    def get_all_people(self):
        return self.db.query(People).all()

    def create_people(self, surname: str = None, name: str = None, patronymic: str = None, sex: str = None, region_id: int = None):
        if region_id is not None and region_id in [region.id for region in self.db.query(Regions).all()]:
            people = People(surname=surname, name=name, patronymic=patronymic, sex=sex, region_id=region_id)
            self.db.add(people)
            self.db.commit()
            self.db.refresh(people)
            return people
        else:
            return None

    def update_people_region(self, id: int, region_id: int):
        people = self.get_people_by_id(id)
        if region_id in [region.id for region in self.db.query(Regions).all()]:
            if people:
                people.region_id = region_id
                self.db.commit()
                self.db.refresh(people)
                return people
            else:
                return 0
        else:
            return 1

    def update_people_delete_region(self, id: int):
        people = self.get_people_by_id(id)
        if people:
            people.region_id = None
            self.db.commit()
            self.db.refresh(people)
            return people

    def update_people_s_n_p(self, id: int, surname: str, name: str, patronymic: str):
        people = self.get_people_by_id(id)
        if people:
            people.surname = surname
            people.name = name
            people.patronymic = patronymic
            self.db.commit()
            self.db.refresh(people)
            return people

    def delete_people(self, id: int):
        people = self.get_people_by_id(id)
        if people:
            self.db.delete(people)
            self.db.commit()
            return True
        return False

    def delete_people_by_region(self, region_id: int):
        peoples = self.db.query(People).filter(People.region_id == region_id).all()
        if peoples:
            for p in peoples:
                self.db.delete(p)
            self.db.commit()
            return True
        return False


class RegionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_region_by_id(self, id: int):
        return self.db.query(Regions).filter(Regions.id == id).first()

    def get_all_regions(self):
        return self.db.query(Regions).all()

    def create_region(self, region_name: str):
        region = Regions(region_name=region_name)
        self.db.add(region)
        self.db.commit()
        self.db.refresh(region)
        return region

    def update_region(self, id: int, region_name: str):
        region = self.get_region_by_id(id)
        if region:
            region.region_name = region_name
            self.db.commit()
            self.db.refresh(region)
            return region
        
    def delete_region(self, id: int):
        region = self.get_region_by_id(id)
        if region:
            self.db.delete(region)
            self.db.commit()
            return True
        return False
