"""
This file has a context manager for managing database sessions and 
functions to contact the database.

Functions:
    1) Session context manager.
    2) Update `games` table with new games.
    3) Update `frames` (frame count) for every game in `games` table.
    4) Find a category (game ID) with minimum amount of frames.
    5) Add frame information to `frames` table.
    6) Get game name from game ID. (not used)
"""

from contextlib import contextmanager

from data.db import Session
from data.db import Game, Frame


@contextmanager
def sessionScope():
    """
    Provide a transactional scope around a series of operations.
    
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
    Update `games` table with `games` dictionary of format:
    {game_id: game_name}
    """

    for game in games:
        
        id = game
        name = games[game]

        """Check if the game already exists in the database."""
        if not session.query(Game).filter_by(id=id).all():

            """Insert the game in the table."""
            game = Game(id=id, name=name, frames=0)
            session.add(game)


def updateFrameCount(session):
    """Update `frames` (frame count) for every game in `games` table."""

    """Get all games."""
    for game in session.query(Game).all():

        """Get game frame amount."""
        frames = session.query(Frame).filter_by(game_id=game.id).count()

        """Update game `frames`."""
        session.query(Game).filter_by(id=game.id).\
            update({Game.frames: frames}, synchronize_session=False)


def minDataCategory(session):
    """Find a category (game ID) with a minimum amount of frames."""

    return session.query(Game.id).order_by(Game.frames).first()[0]


def addFrame(session, path, gameID, login):
    """Add frame information to `frames` table."""

    frame = Frame(path=path, game_id=gameID, user_login=login)
    session.add(frame)


def gameIDtoName(session, gameID):
    """Converts game ID to name."""

    return session.query(Game.name).filter_by(id=gameID).first()[0]
