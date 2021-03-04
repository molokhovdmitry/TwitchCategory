"""
This file will have functions to contact with database.

Functions:
Update categories (`games` table)
Choose category with the least amount of data (`game_frames` table)
Add frame to database (`frames` table, `game_frames` table)
"""

from db import Session
from db import Game, Frame, GameFrames

from contextlib import contextmanager

@contextmanager
def sessionScope():
    """Provide a transactional scope around a series of operation."""
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
    Updates `games` table.

    `games` input is a dictionary of format:
    {game_id: game_name}
    """
    for game in games:
        
        id = game
        name = games[game]

        # Check if it already exists in the database
        if not session.query(Game).filter_by(id=id).all():

            # Insert `game` and `id` if not exist
            game = Game(id=id, name=name)
            session.add(game)
    
    # Print all games
    for game in session.query(Game).all():
        print(game)

def minDataCategory(session):
    """Finds a category (game ID) with minimum amount of frames."""

    return session.query(GameFrames.game_id).\
           order_by(GameFrames.frame_count).first()[0]

    """
    game1 = GameFrames(game_id="1654", frame_count="1234")
    game3 = GameFrames(game_id="29975", frame_count="0")
    game2 = GameFrames(game_id="19554", frame_count="23453245")

    session.add_all([game1, game3, game2])

    # Print
    for game in session.query(GameFrames).all():
        print(game)
    """



def addFrame(session, path, game_id, user_name):
    """Updates `frames` table """

    frame = Frame(path=path, game_id=game_id, user_name=user_name)

    session.add(frame)

    """
    # Print
    for frame in session.query(Frame).all():
        print(frame)
    """
