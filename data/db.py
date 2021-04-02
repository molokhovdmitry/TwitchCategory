"""
This file connects to a database and creates tables if they don't exist.

Made with:
https://docs.sqlalchemy.org/en/13/orm/tutorial.html#object-relational-tutorial
"""

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker


"""Connect to postgres database."""
from config import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD

DATABASE = {
    'drivername': 'postgres',
    'host': DB_HOST,
    'port': DB_PORT,
    'username': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME
}


engine = create_engine(URL(**DATABASE), echo=False)
Session = sessionmaker(bind=engine)


"""Create schema."""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, DateTime

from datetime import datetime

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    frames = Column(Integer)

    def __repr__(self):
        return f"<Game(" + \
                        f"id='{self.id}', " + \
                        f"name='{self.name}', " + \
                        f"frames='{self.frames}'" + \
                ")>"

class Frame(Base):
    __tablename__ = "frames"

    id = Column(Integer, primary_key=True)
    path = Column(String)
    game_id = Column(Integer, ForeignKey(Game.id))
    user_login = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Frame(" + \
                        f"id='{self.id}'," + \
                        f"path='{self.path}'," + \
                        f"game_id='{self.game_id}', " + \
                        f"user_login='{self.user_login}'," + \
                        f"date='{self.date}'" + \
                ")>"


"""Create tables if they don't exist."""
Base.metadata.create_all(engine)
