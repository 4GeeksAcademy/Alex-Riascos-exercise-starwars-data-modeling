import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

# Tablas intermedias
vehicle_character = Table('vehicle_character', Base.metadata,
    Column('vehicle_id', Integer, ForeignKey('vehicle.id'), primary_key=True),
    Column('character_id', Integer, ForeignKey('character.id'), primary_key=True)
)

movie_character = Table('movie_character', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id'), primary_key=True),
    Column('character_id', Integer, ForeignKey('character.id'), primary_key=True)
)

planet_character = Table('planet_character', Base.metadata,
    Column('planet_id', Integer, ForeignKey('planet.id'), primary_key=True),
    Column('character_id', Integer, ForeignKey('character.id'), primary_key=True)
)

vehicle_planet = Table('vehicle_planet', Base.metadata,
    Column('vehicle_id', Integer, ForeignKey('vehicle.id'), primary_key=True),
    Column('planet_id', Integer, ForeignKey('planet.id'), primary_key=True)
)

movie_planet = Table('movie_planet', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id'), primary_key=True),
    Column('planet_id', Integer, ForeignKey('planet.id'), primary_key=True)
)

movie_vehicle = Table('movie_vehicle', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movie.id'), primary_key=True),
    Column('vehicle_id', Integer, ForeignKey('vehicle.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    name = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    suscription_date = Column(Date, nullable=False)
    favorite_movies = relationship("Favorite_movie", back_populates="user")
    favorite_planets = relationship("Favorite_planet", back_populates="user")
    favorite_characters = relationship("Favorite_character", back_populates="user")
    favorite_vehicles = relationship("Favorite_vehicle", back_populates="user")

class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True)
    planet_name = Column(String(250), nullable=False)
    diameter = Column(String(250), nullable=False)
    rotation_period = Column(String(250), nullable=False)
    orbital_period = Column(String(250), nullable=False)
    gravity = Column(String(250), nullable=False)
    population = Column(String(250), nullable=False)
    climate = Column(String(250), nullable=False)
    terrain = Column(String(250), nullable=False)       
    favorites = relationship("Favorite_planet", back_populates="planet")

class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    height = Column(String(250), nullable=False)
    mass = Column(String(250), nullable=False)  
    hair_color = Column(String(250), nullable=False)
    age = Column(Integer, nullable=False)
    homeworld = Column(String(250), nullable=False)
    favorites = relationship("Favorite_character", back_populates="character")

class Vehicle(Base):
    __tablename__ = 'vehicle'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    model = Column(String(250), nullable=False)    
    length = Column(String(250), nullable=False)
    max_atmosphering_speed = Column(String(250), nullable=False)    
    passengers = Column(String(250), nullable=False)       
    vehicle_class = Column(String(250), nullable=False)
    favorites = relationship("Favorite_vehicle", back_populates="vehicle") 

class Movie(Base):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    episode_id = Column(Integer, nullable=False)
    opening_crawl = Column(String(250), nullable=False)
    director = Column(String(250), nullable=False)
    producer = Column(String(250), nullable=False)
    release_date = Column(Date, nullable=False)    
    favorites = relationship("Favorite_movie", back_populates="movie")

class Favorite_movie(Base):
    __tablename__ = 'favorite_movie'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="favorite_movies")
    movie_id = Column(Integer, ForeignKey('movie.id'))
    movie = relationship("Movie", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "movie": self.movie.serialize()
        }

class Favorite_planet(Base):
    __tablename__ = 'favorite_planet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="favorite_planets")
    planet_id = Column(Integer, ForeignKey('planet.id'))
    planet = relationship("Planet", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "planet": self.planet.serialize()
        }

class Favorite_character(Base):
    __tablename__ = 'favorite_character'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="favorite_characters")
    character_id = Column(Integer, ForeignKey('character.id'))
    character = relationship("Character", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "character": self.character.serialize()
        }

class Favorite_vehicle(Base):
    __tablename__ = 'favorite_vehicle'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="favorite_vehicles")
    vehicle_id = Column(Integer, ForeignKey('vehicle.id'))
    vehicle = relationship("Vehicle", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle_id": self.vehicle_id,
            "vehicle": self.vehicle.serialize()
        }

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
