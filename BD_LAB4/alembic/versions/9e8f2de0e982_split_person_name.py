"""split_person_name

Revision ID: 9e8f2de0e982
Revises: 51e4c6afd79f
Create Date: 2023-11-12 23:49:40.221202

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
    patronymic = sa.Column(sa.String, nullable=False)
    surname = sa.Column(sa.String, nullable=False)


# revision identifiers, used by Alembic.
revision: str = '9e8f2de0e982'
down_revision: Union[str, None] = '51e4c6afd79f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    op.add_column('person', sa.Column('surname', sa.String))
    op.add_column('person', sa.Column('patronymic', sa.String))

    peoples = session.query(Person).all()
    for person in peoples:
        surname_u, name_u, patronymic_u = person.name.split(' ')
        person.surname = surname_u
        person.name = name_u
        person.patronymic = patronymic_u

    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    peoples = session.query(Person).all()
    for person in peoples:
        person.name = person.surname + " " + person.name + " " + person.patronymic

    op.drop_column('person', 'surname')
    op.drop_column('person', 'patronymic')
    session.commit()
