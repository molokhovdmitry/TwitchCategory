"""
This file will interact with a database.

Functions:
Create tables if they don't exist
Update categories (`games` table)
Choose category with the least amount of data (`game_frames` table)
Add frame to database (`frames` table, `game_frames` table)
"""
import sqlalchemy
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date
from config import DB_USER, DB_PASSWORD

from datetime import datetime

# Connect to postgres database
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



# Create tables
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


from sqlalchemy import Column, Integer, String, DateTime

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<Game(" + \
                        f"id='{self.id}', " + \
                        f"name='{self.name}'" + \
                ")>"

class Frame(Base):
    __tablename__ = "frames"

    id = Column(Integer, primary_key=True)
    path = Column(String)
    game_id = Column(Integer, ForeignKey(Game.id))
    user_name = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Frame(" + \
                        f"id='{self.id}'," + \
                        f"path='{self.path}'," + \
                        f"game_id='{self.game_id}', " + \
                        f"user_name='{self.user_name}'," + \
                        f"date='{self.date}'" + \
                ")>"

class GameFrames(Base):
    __tablename__ = "game_frames"

    game_id = Column(Integer, ForeignKey(Game.id), primary_key=True)
    frame_count = Column(Integer)

    def __repr__(self):
        return f"<GameFrames(" + \
                        f"game_id='{self.game_id}'," + \
                        f"frame_count='{self.frame_count}'" + \
                ")>"

Base.metadata.create_all(engine)

"""
session = Session()

# Games
gta = Game(name="GTA_5")
minecraft = Game(name="Minecraft")

# Frames
frame_1 = Frame(path="/asdf/gsdf/1.png", game_id=1, user_name="forsen")
frame_2 = Frame(path="/asdf/gsdf/2.png", game_id=1, user_name="nymn")
frame_3 = Frame(path="/asdf/gsdf/3.png", game_id=1, user_name="forsen")
frame_4 = Frame(path="/asdf/gsdf/4.png", game_id=1, user_name="nymn")
frame_5 = Frame(path="/asdf/gsdf/5.png", game_id=2, user_name="forsen")
frame_7 = Frame(path="/asdf/gsdf/7.png", game_id=2, user_name="nymn")
frame_8 = Frame(path="/asdf/gsdf/8.png", game_id=2, user_name="forsen")

session.add_all([gta, minecraft, frame_1, frame_2, frame_3, frame_4, frame_5,
                frame_7, frame_8])

session.commit()

# Game frames
gta_frames = GameFrames(game_id=1, frame_count=4)
minecraft_frames = GameFrames(game_id=2, frame_count=4)
session.add_all([gta_frames, minecraft_frames])

session.commit()

# Drop tables
GameFrames.__table__.drop(engine)
Frame.__table__.drop(engine)
Game.__table__.drop(engine)
session.commit()

for game in session.query(Game).all():
    print(game)

for frame in session.query(Frame).all():
    print(frame)

for gameFrames in session.query(GameFrames).all():
    print(gameFrames)
"""