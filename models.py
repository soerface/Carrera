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
    date = Column(DateTime)
    rounds = relationship('Round', backref='race')

    def __init__(self):
        pass

    def __repr__(self):
        return '<Race {0}>'.format(self.time)

class Round(Base):
    __tablename__ = 'rounds'

    id = Column(Integer, primary_key=True)
    num = Column(Integer)
    player_id = Column(Integer, ForeignKey('players.id'))
    player = relationship('Player')
    time = Column(Time)
    race_id = Column(Integer, ForeignKey('races.id'))

    def __init__(self, num, time, player=None):
        self.num = num
        self.time = time
        self.player = player

    def __repr__(self):
        name = self.player.name if self.player else 'Unknown'
        return '<Round {num} by {player}>'.format(num=self.num, player=name)
