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
This file downloads frames from streams in top categories of twitch.

Pseudocode:
    while `Enter` is not pressed:
        Loop:
        1) Get top games from twitch api, save them in a database.
        2) Get a game with a minimum number of saved frames.
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

from data.downloadFuncs import downloadFrames
from data.api import *
from data.dbFuncs import *

from config import DOWNLOAD_PATH
DATA_PATH = Path.joinpath(Path(DOWNLOAD_PATH), "frames")


def updateData():
    """Update data while no input (Enter not pressed)."""

    """Start helper threads."""
    inputList = []
    Thread(target=inputThread, args=(inputList, )).start()
    Thread(target=infoThread, args=(inputList, )).start()
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

            """Get a category with a minimum number of frames."""
            gameID = minDataCategory(dbSession)[0]

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


def infoThread(inputList):
    """
    Thread that shows how much data is downloaded and min/max data categories
    every `n` seconds.
    """

    n = 1200

    """Print data size."""
    print(colored(dirSize(DATA_PATH), 'green'))

    """Print categories with minumum and maximum number of frames."""
    printMinMax()

    """Repeat every `n` seconds."""
    i = 0
    while not inputList:
        if i != n:
            time.sleep(1)
            i += 1
            continue
        i = 0

        print(colored(dirSize(DATA_PATH), 'green'))
        printMinMax()


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


def printMinMax():
    """Print categories with minumum and maximum number of frames."""

    with sessionScope() as dbSession:
        minCategory = minDataCategory(dbSession)
        maxCategory = maxDataCategory(dbSession)

    print(colored("Minimum: {} frames in category {}."
                    .format(minCategory[1], minCategory[0]),
                    'green'))
    print(colored("Maximum: {} frames in category {}."
                    .format(maxCategory[1], maxCategory[0]),
                    'green'))


if __name__ == "__main__":
    updateData()
