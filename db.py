import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PG_USERNAME = os.environ['PG_USERNAME']
PG_PASSWORD = os.environ['PG_PASSWORD']
PG_HOST = os.environ['PG_HOST']

# Define the engine. This has a default connection pool.
engine = create_engine('postgresql+psycopg2://%s:%s@%s/users' % (PG_USERNAME, PG_PASSWORD, PG_HOST))

# Session object bound to the engine
Session = sessionmaker(bind=engine)


def get_session():
    """
    Instantiate and return a session

    :return: db Session
    """

    return Session()
