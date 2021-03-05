"""
This file has a context manager for managing database sessions and 
functions to contact the database:
    1) Update `games` table.
    2) Find a category (game ID) with minimum amount of frames.
    3) Add frame's information to `frames` table.
"""

from db import Session
from db import Game, Frame, GameFrames

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
    Update `games` table.

    `games` input is a dictionary of format:
    {game_id: game_name}
    """

    for game in games:
        
        id = game
        name = games[game]

        # Check if it already exists in the database
        if not session.query(Game).filter_by(id=id).all():

            # Insert `game` and `id` if not exists
            game = Game(id=id, name=name)
            session.add(game)


def minDataCategory(session):
    """Find a category (game ID) with minimum amount of frames."""

    return session.query(GameFrames.game_id).\
           order_by(GameFrames.frame_count).first()[0]


def addFrame(session, path, game_id, user_name):
    """Add frame information to `frames` table."""

    frame = Frame(path=path, game_id=game_id, user_name=user_name)
    session.add(frame)
