"""
This file has a context manager for managing database sessions and 
functions to contact the database:
    1) Update `games` table.
    2) Find a category (game ID) with minimum amount of frames.
    3) Add frame's information to `frames` table.
"""

from db import Session
from db import Game, Frame

from contextlib import contextmanager

@contextmanager
def sessionScope():
    """
    Provide a transactional scope around a series of operation.
    
    This context manager constructs a session, commits transactions and
    closes the session.    
    https://docs.sqlalchemy.org/en/13/orm/session_basics.html#session-faq-whentocreate
    """

    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def updateGames(session, games):
    """
    Update `games` and `game_frames` table.

    `games` input is a dictionary of format:
    {game_id: game_name}
    """

    for game in games:
        
        id = game
        name = games[game]

        # Check if it already exists in the database
        if session.query(Game).filter_by(id=id).all():

            # Get frame amount
            frames = session.query(Frame).filter_by(game_id=id).count()

            # Update frames
            session.query(Game).filter_by(id=id).\
                update({Game.frames: frames}, synchronize_session=False)
        
        else:
            # Insert game in tables if not exists
            game = Game(id=id, name=name, frames=0)
            session.add(game)


def minDataCategory(session):
    """Find a category (game ID) with minimum amount of frames."""

    return session.query(Game.id).order_by(Game.frames).first()[0]


def addFrame(session, path, game_id, user_name):
    """Add frame information to `frames` table."""

    frame = Frame(path=path, game_id=game_id, user_name=user_name)
    session.add(frame)
