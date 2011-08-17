from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

def connect_db(filename='dev.db'):
    """Cares about database connection and returns a session.

    Takes

    """
    engine = create_engine('sqlite:///{0}'.format(filename))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
