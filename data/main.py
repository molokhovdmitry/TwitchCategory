"""
This file downloads frames from streams in top categories of twitch.

Pseudocode:
    while `Enter` is not pressed:
        Loop:
        1) Get top games from twitch api, save them in a database.
        2) Get a game with the least amount of saved frames.
        3) Get logins of streams that are live in that category.
        4) Download frames from 5 random streams,
        save frame info in the database.
"""

import random
import time
import requests
from threading import Thread
from pathlib import Path
from termcolor import colored

from streamlink import Streamlink

from data.download import downloadFrames
from data.api import *
from data.dbFuncs import *

from config import DOWNLOAD_PATH
DATA_PATH = Path.joinpath(Path(DOWNLOAD_PATH), "frames")


def updateData():
    """Update data while no input (Enter not pressed)."""

    """Start helper threads."""
    inputList = []
    Thread(target=inputThread, args=(inputList, )).start()
    Thread(target=sizeThread, args=(inputList, )).start()
    print("Press Enter any time to stop downloading.")

    """Start a streamlink session."""
    streamlinkSession = Streamlink()

    """Start an api session."""
    apiSession = requests.session()

    downloadedStreams = 0
    failCount = 0
    frameCount = 0
    while not inputList:

        """Update top categories."""
        games = getTopGames(apiSession)
        if not games:
            print("Error. Could not get top games.")
            continue
        
        """Start a database session."""
        with sessionScope() as dbSession:

            """Update the database."""
            updateGames(dbSession, games)
            updateFrameCount(dbSession)

            """Get a category with the least data."""
            gameID = minDataCategory(dbSession)

        """Get streams from the category."""
        streams = getStreams(apiSession, gameID)
        if not streams:
            print("Error. Could not get streams.")
            continue

        """Update the category (download frames 5 times)."""
        downloadCount = 0
        downloadAttempts = 0
        while streams and downloadCount < 5 and downloadAttempts < 10:

            if inputList:
                break

            """Get a random stream."""
            stream = random.choice(list(streams))
            streams.discard(stream)


            """Download frames from a stream, update the database."""
            print(f"Downloading frames from '{stream}', gameID: {gameID}.")
            download = False
            for framePath in downloadFrames(streamlinkSession, stream, gameID):

                """Save a frame in the database."""
                with sessionScope() as dbSession:
                    addFrame(dbSession, framePath, gameID, stream)
                    print(f"{framePath} saved.")

                download = True
                frameCount += 1
            
            downloadCount += download
            downloadAttempts += 1

            downloadedStreams += download
            failCount += not download
                

    """Update the database."""
    with sessionScope() as dbSession:
        updateFrameCount(dbSession)

    print("Done.")
    print(f"Downloaded {frameCount} frame(s) from {downloadedStreams} stream(s)." + \
        f" Failed {failCount} time(s).")


def inputThread(inputList):
    """Thread that waits for an input."""

    input()
    inputList.append(True)
    print(colored("Interrupting. Please wait.", 'green'))


def sizeThread(inputList):
    """Thread that shows how much data is downloaded every 120 seconds."""

    print(colored(dirSize(DATA_PATH), 'green'))
    n = 0
    while not inputList:
        if n != 120:
            time.sleep(1)
            n += 1
            continue
        n = 0

        print(colored(dirSize(DATA_PATH), 'green'))


def dirSize(path):
    """Return the size of `path` folder."""

    files = list(path.glob('**/*'))
    size = 0
    for file in files:
        if file.is_file():
            size += file.stat().st_size

    """Convert to GB."""
    size = size / 1073741824
    
    return "Data size: " + '{:.2f}'.format(size) + " GB"


if __name__ == "__main__":
    updateData()
