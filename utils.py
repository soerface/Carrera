from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

def connect_db(filename=':memory:'):
    """Cares about database connection and returns a session.

    Takes the filename for the databse, default memory.

    """
    engine = create_engine('sqlite:///{0}'.format(filename))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def trim_time(time):
    """Rounds the time to 3 digits after the comma and returns it as a string"""
    return '{0:.3f}'.format(time)
