from sqlalchemy import Table, Column, Integer, ForeignKey
from . import Base

# Association table
event_sub_weapon_type = Table(
    'event_sub_weapon_type', Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('event_id', Integer, ForeignKey('events.id')),
    Column('sub_weapon_type_id', Integer, ForeignKey('sub_weapon_type.id'))
)