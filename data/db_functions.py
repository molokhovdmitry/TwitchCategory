"""
MIT License

Copyright (c) 2021 molokhovdmitry

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
This file has a context manager for managing database sessions and 
functions to contact the database.  

Functions:  
    1) Session context manager.  
    2) Update `games` table with new games.  
    3) Update `frames` (frame count) for every game in `games` table.  
    4) Find a category (game ID) with minimum number of frames.  
    5) Get game ID and frame count for a category with a minimum
    number of frames.  
    6) Get game ID and frame count for a category with a maximum
    number of frames.  
    7) Add frame information to `frames` table.  
    8) Get game name from game ID. (not used)  
    9) Delete frames from `frames` table that are were from the
    downloaded data.
"""

from contextlib import contextmanager
from pathlib import Path

from data.db import Session
from data.db import Game, Frame

from config import DOWNLOAD_PATH, MAX_GAMES

DATA_PATH = Path.joinpath(Path(DOWNLOAD_PATH), "frames")

@contextmanager
def session_scope():
    """
    Provides a transactional scope around a series of operations.  
    
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


def update_games(session, games):
    """
    Updates `games` table with `games` dictionary of format:
    {game_id: game_name}
    """
    game_count = get_game_count(session)

    for game in games:
        
        id = game
        name = games[game]

        # Check if the game already exists in the database and game limit
        # is not exceeded.
        if (not session.query(Game).filter_by(id=id).all()
            and game_count < MAX_GAMES):

            # Insert the game in the table.
            game = Game(id=id, name=name, frames=0)
            session.add(game)

            game_count += 1


def get_game_count(session):
    """Returns the number of games in the `games` table."""
    return len(session.query(Game).all())


def update_frame_count(session):
    """Updates `frames` (frame count) for every game in `games` table."""
    # Get all games.
    for game in session.query(Game).all():

        # Get game frame number.
        frames = session.query(Frame).filter_by(game_id=game.id).count()

        # Update game `frames`.
        game = session.query(Game).filter_by(id=game.id).one()
        game.frames = frames


def min_data_category(session):
    """
    Returns game ID and frame count for a category with a minimum
    number of frames.
    """
    # Ensure the table is not empty.
    if session.query(Game).all():

        # Get game ID and frame count.
        game_id, frame_count = session.query(Game.id, Game.frames).\
                                     order_by(Game.frames).first()
    else:
        return None

    return game_id, frame_count


def max_data_category(session):
    """
    Returns game ID and frame count for a category with a maximum
    number of frames.
    """
    # Ensure the table is not empty.
    if session.query(Game).all():

        # Get game ID and frame count.
        game_id, frame_count = session.query(Game.id, Game.frames).\
                                     order_by(Game.frames.desc()).first()
    else:
        return None

    return game_id, frame_count


def add_frame(session, path, game_id, login):
    """
    Adds frame information to `frames` table, updates `frames` column
    in `games` table.
    """
    # Update `frames` table.
    frame = Frame(path=path, game_id=game_id, user_login=login)
    session.add(frame)

    # Update `games` table.
    game = session.query(Game).filter_by(id=game_id).one()
    game.frames += 1


def game_id_to_name(session, gameID):
    """Converts game ID to name."""
    return session.query(Game.name).filter_by(id=gameID).one()[0]


def sync_db(session):
    """
    Deletes categories from `games` table and frames from `frames` table that
    were deleted from the downloaded data.  
    
    Also deletes categories, frames for which weren't downloaded yet.  

    Used for updating the database after data cleaning.
    """
    data_path = DATA_PATH
    categories = list(p.name for p in data_path.glob('*'))

    # Get downloaded frames.
    frames = dict()
    for category in categories:
        category_path = Path.joinpath(data_path, category)
        category_frames = [p.name for p in category_path.glob('*')]
        frames[category] = category_frames
    
    # Delete removed categories from the database.
    for game in session.query(Game).all():

        if game.id not in list(map(int, categories)):

            # Delete all frames in that category.
            for frame in session.query(Frame).filter_by(game_id=game.id).all():
                session.delete(frame)

            session.commit()
            
            # Delete category from `games` table.
            session.delete(game)

    # Delete removed frames from the database.
    for frame in session.query(Frame).all():
        if Path(frame.path).name not in frames[str(frame.game_id)]:
            session.delete(frame)
