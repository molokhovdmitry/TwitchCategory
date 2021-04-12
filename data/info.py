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
This file prints information about the database and a list of all games.
"""

from pathlib import Path
import requests

from data.download import printDatasetInfo
from data.api import gameIDtoName

from config import DOWNLOAD_PATH

dataPath = Path.joinpath(Path(DOWNLOAD_PATH), "frames")

def info():
    """Prints info and a list of games."""

    printDatasetInfo()
    printGames()


def printGames():
    """Prints all games from the dataset."""

    """Get game IDs."""
    gameIDs = list(p.name for p in dataPath.glob('*'))

    """Get game names."""
    apiSession = requests.session()
    games = dict()
    for gameID in gameIDs:
        games[gameID] = gameIDtoName(apiSession, gameID)
    
    """Print in alphabetical order."""
    for gameID in sorted(games, key=games.get):
        print(f"{games[gameID]}, game ID: {gameID}.")

if __name__ == "__main__":
    info()
