"""create_region_table

Revision ID: a2ee97efdb40
Revises: 9e8f2de0e982
Create Date: 2023-11-12 23:49:46.181672

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
    region_id = sa.Column(sa.Integer, sa.ForeignKey('region.id', name='fk_person_region_id'))

class Region(Base):
    __tablename__ = 'region'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)

# revision identifiers, used by Alembic.
revision: str = 'a2ee97efdb40'
down_revision: Union[str, None] = '9e8f2de0e982'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    Region.__table__.create(bind)

    region = Region(name = 'Донецк')
    session.add(region)

    region = Region(name= 'Луганск')
    session.add(region)

    region = Region(name= 'Бахмут')
    session.add(region)

    with op.batch_alter_table('person') as batch_op:
        batch_op.add_column(sa.Column('region_id', sa.Integer, sa.ForeignKey('region.id', name='fk_person_region_id')))

    peoples = session.query(Person).all()
    regions = session.query(Region).all()
    
    for person in peoples:
        for region in regions:
            if person.address == region.name:
                person.region_id = region.id
                break

    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    with op.batch_alter_table('person') as batch_op:
        batch_op.drop_column('region_id')
    op.drop_table('region')
