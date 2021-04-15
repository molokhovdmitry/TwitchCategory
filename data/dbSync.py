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
This file updates the database after data cleaning.
"""

from data.db import Game, Frame
from data.dbFuncs import syncDB, updateFrameCount, sessionScope

def sync():
    """
    Deletes categories from `games` table and frames from `frames` table that
    were deleted from the downloaded data and prints the number of deleted
    categories and frames.
    """

    with sessionScope() as session:

        gamesBefore = len(session.query(Game).all())
        framesBefore = len(session.query(Frame).all())

        """Update the database."""
        syncDB(session)
        updateFrameCount(session)

        gamesAfter = len(session.query(Game).all())
        framesAfter = len(session.query(Frame).all())

        deletedGames = gamesBefore - gamesAfter
        deletedFrames = framesBefore - framesAfter
        
        
    print(f"Deleted {deletedGames} game(s) and {deletedFrames} frame(s) "
           "from the database.")


if __name__ == "__main__":
    sync()
