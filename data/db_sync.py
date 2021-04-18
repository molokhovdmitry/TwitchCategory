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

"""This file updates the database after data cleaning."""

from data.db import Game, Frame
from data.db_functions import sync_db, update_frame_count, session_scope

def sync():
    """
    Deletes categories from `games` table and frames from `frames` table that
    were deleted from the downloaded data and prints the number of deleted
    categories and frames.
    """

    with session_scope() as session:

        games_before = len(session.query(Game).all())
        frames_before = len(session.query(Frame).all())

        # Update the database.
        sync_db(session)
        update_frame_count(session)

        games_after = len(session.query(Game).all())
        frames_after = len(session.query(Frame).all())

    deleted_games = games_before - games_after
    deleted_frames = frames_before - frames_after

    print(f"Deleted {deleted_games} game(s) and {deleted_frames} frame(s) "
           "from the database.")


if __name__ == "__main__":
    sync()
