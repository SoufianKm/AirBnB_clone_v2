#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity


"""
instance of SQLAlchemy Table represents
the relationship `Many-to-Many` between
Place and Amenity.
"""
place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column(
            'place_id',
            String(60),
            ForeignKey('places.id'),
            nullable=False,
            primary_key=True),
        Column(
            'amenity_id',
            String(60),
            ForeignKey('amenities.id'),
            nullable=False,
            primary_key=True)
)


class Place(BaseModel, Base):
    """ A place to stay

    Attributes:
        __tablename__: Table name, places
        city_id: Id of city
        user_id: Id user
        name: Place name
        description: Place description
        number_rooms: Integer number of room
        number_bathrooms: Integer number of bathrooms
        max_guest: Integer maximum guest
        price_by_night: Integer price by night
        latitude: Float latitude
        longitude: Float longitude
        reviews: represent a relationship with the class Review
        amenities: represent a relationship with the class Amenity
        amenity_ids: list of Amenity ids
    """
    __tablename__ = 'places'

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship('Review', cascade="all, delete, \
                delete-orphan", backref='place')
        amenities = relationship(
                'Amenity',
                secondary=place_amenity,
                viewonly=False,
                backref='place_amenities')
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0

        @property
        def reviews(self):
            """Returns the list of Review of Place"""
            from models import storage
            place_reviews = []
            for value in storage.all(Review).values():
                if value.place_id == self.id:
                    place_reviews.append(value)
            return place_reviews

        @property
        def amenities(self):
            """Returns the amenities of this Place"""
            from models import storage
            amenities_of_place = []
            for value in storage.all(Amenity).values():
                if value.id in self.amenity_ids:
                    amenities_of_place.append(value)
            return amenities_of_place

        @amenities.setter
        def amenities(self, value):
            """Adds an amenity to this Place"""
            if type(value) is Amenity:
                if value.id not in self.amenity_ids:
                    self.amenity_ids.append(value.id)

    amenity_ids = []
