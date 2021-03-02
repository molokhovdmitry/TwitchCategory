"""
This file will interact with a database.

Functions:
Create tables if they don't exist
Update categories (`games` table)
Choose category with the least amount of data (`game_frames` table)
Add frame to database (`frames` table, `game_frames` table)
"""
# Connect to postgres database
import sqlalchemy
from config import DB_USER, DB_PASSWORD

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': DB_USER,
    'password': DB_PASSWORD,
    'database': 'mydb'
}


from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import session, sessionmaker

engine = create_engine(URL(**DATABASE), echo=True)
Session = sessionmaker(bind=engine)


from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


from sqlalchemy import Column, Integer, String, DateTime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(DateTime)

    def __repr__(self):
        return "<User(name='%s')>" % (self.name)

# Create table(s) if they don't exist
Base.metadata.create_all(engine)

session = Session()

"""
ed_user = User(name="ed")
session.add(ed_user)
"""
for user in session.query(User).all():
    print(user)

session.commit()
