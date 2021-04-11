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
