from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#this is the connection string that we used to pass to the sqlalchemy
SQLALCHEMY_DATABASE_URL='postgresql://postgres:postgres@localhost:5433/fastmedia'

#this engine is responisble for establishing the connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#if we want to talk to the database we have to use session
SessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)

#to create the models
Base = declarative_base()

#method to get the db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()