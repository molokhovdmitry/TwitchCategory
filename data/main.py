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
import threading
from pathlib import Path
from termcolor import colored

from streamlink import Streamlink

from data.download import downloadFrames
from data.api import *
from data.dbFuncs import *

from config import DOWNLOAD_PATH
DATA_PATH = Path.joinpath(Path(DOWNLOAD_PATH), "frames")

"""
Make a thread that will stop the while loop on input.
"""

def inputThread(inputList):
    """Thread that waits for an input."""

    input()
    inputList.append(True)
    print("Interrupting. Please wait.")

def sizeThread():
    """Thread that shows how much data is downloaded every 120 seconds."""
    while not inputList:

        files = list(DATA_PATH.glob('**/*'))
        size = 0
        for file in files:
            if file.is_file():
                size += file.stat().st_size

        """Convert to GB."""
        size = size / 1073741824

        print(colored("Data size: " + '{:.2f}'.format(size) + " GB", 'green'))
        time.sleep(120)


"""Start a thread that updates `inputList` with inputs."""
inputList = []
threading.Thread(target=inputThread, args=(inputList, )).start()
threading.Thread(target=sizeThread).start()
print("Press Enter any time to stop downloading.")
time.sleep(3)


"""Update data while no input (Enter not pressed)."""
downloadCountGlobal = 0
failCount = 0
frameCount = 0

"""Start a streamlink session."""
streamlinkSession = Streamlink()
"""Start an api session."""
apiSession = requests.session()

while not inputList:

    """Update top categories."""
    games = getTopGames(apiSession)
    if not games:
        print("Error. Could not get top games.")
        continue
    
    """Start a database session."""
    with sessionScope() as session:

        """Update the database."""
        updateGames(session, games)
        updateFrameCount(session)

        """Get a category with the least data."""
        gameID = minDataCategory(session)

    """Update the category (download frames 5 times)."""
    
    downloadCount = 0
    downloadAttempts = 0

    """Get streams from the category."""
    streams = getStreams(apiSession, gameID)
    if not streams:
        print("Error. Could not get streams.")
        continue

    while streams and downloadCount < 5 and downloadAttempts < 10:

        """Get a random stream."""
        stream = random.choice(list(streams))
        streams.discard(stream)

        print(f"Downloading frames from '{stream}', gameID: {gameID}.")

        """Download frames from a stream, update the database."""
        download = False
        for framePath in downloadFrames(streamlinkSession, stream, gameID):

            """Save the frame in the database."""
            with sessionScope() as session:
                addFrame(session, framePath, gameID, stream)

            download = True
            frameCount += 1
        
        downloadCount += download
        downloadAttempts += 1

        downloadCountGlobal += download
        failCount += not download
            

"""Update the database."""
with sessionScope() as session:
    updateFrameCount(session)

print("Done.")
print(f"Downloaded {frameCount} frames from {downloadCountGlobal} stream(s)." + \
      f" Failed {failCount} time(s).")
