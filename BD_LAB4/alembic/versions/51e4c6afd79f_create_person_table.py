"""create_person_table

Revision ID: 51e4c6afd79f
Revises: 
Create Date: 2023-11-12 23:49:21.448578

"""
from typing import Sequence, Union
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from alembic import op
import sqlalchemy as sa

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    address = sa.Column(sa.String, nullable=False)


# revision identifiers, used by Alembic.
revision: str = '51e4c6afd79f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    Person.__table__.create(bind)

    person = Person(name = 'Найданов Павел Нурсултанович', address = 'Бахмут')
    session.add(person)

    person = Person(name= 'Шойгу Сергей Кужугетович', address= 'Донецк')
    session.add(person)

    person = Person(name= 'Зарубанов Владимир Витальевич', address= 'Луганск')
    session.add(person)

    session.commit()

def downgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    
    op.drop_table('person')
    
    session.commit()
