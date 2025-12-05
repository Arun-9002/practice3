
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Database_url = "mysql+mysqlconnector://root@localhost/practice3"

engine = create_engine(Database_url, pool_pre_ping=True)    
sessionlocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
