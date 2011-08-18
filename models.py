from datetime import datetime

from sqlalchemy import Column, Integer, String, Time, DateTime, Table, \
     ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#player_cars_table = Table('player_cars', Base.metadata,
#    Column('player_id', Integer, ForeignKey('players.id')),
#    Column('car_id', Integer, ForeignKey('cars.id')),
#)

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Player {0}>'.format(self.name)

class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Car {0}>'.format(self.name)

class Score(Base):
    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True)
    round_time = Column(Time)
    total_time = Column(Time)
    date = Column(DateTime)
    car_id = Column(Integer, ForeignKey('cars.id'))
    car = relationship('Car')
    player_id = Column(Integer, ForeignKey('players.id'))
    player = relationship('Player', backref='scores')

    def __init__(self, total_time, round_time, player=None, car=None):
        self.total_time = total_time
        self.round_time = round_time
        self.date = datetime.now()
        self.player = player
        self.car = car

    def __repr__(self):
        return '<Score {0}>'.format(self.total_time)

class Race(Base):
    __tablename__ = 'races'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)

    def __init__(self, time):
        self.time = time

    def __repr__(self):
        return '<Race {0}>'.format(self.time)
