#!/usr/bin/python3
""" City Module for HBNB project """
import os
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ City class

    Attributes:
        __tablename__: the table name cities
        state_id: The state id
        name: The city name
        places: relationship with the class Place
    """
    __tablename__ = 'cities'

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship('Place', cascade='all, delete, \
                delete-orphan', backref='cities')
    else:
        name = ''
        state_id = ''
        places = None
