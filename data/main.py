"""
This file gets top viewed games of twitch, adds them to database.
Then it finds the game with the least amount of saved frames and
finds streams in that category. After that it tries to download
frames from 5 random streams.
"""

import random
import time

from data.download import downloadFrames
from data.api import *
from data.dbFuncs import *

"""
Make a thread that will stop the while loop on input.
"""
import threading

def inputThread(inputList):
    """Thread that waits for an input."""
    input()
    inputList.append(True)
    print("Interrupting.")

"""Start a thread that updates `inputList` with inputs."""
inputList = []
threading.Thread(target=inputThread, args=(inputList, )).start()
print("Press Enter to stop downloading.")


"""Update data while no input (Enter not pressed)."""
downloadCountGlobal = 0
failCount = 0
frameCount = 0
while not inputList:
    
    with sessionScope() as session:

        """Update top categories."""
        games = getTopGames()
        if not games:
            print("Error. Could not get top games.")
            time.sleep(5)
            continue
        updateGames(session, games)
        updateFrameCount(session)

        """Get category with least data."""
        gameID = minDataCategory(session)

    """Update category (download frames 5 times)."""
    
    downloadCount = 0
    downloadAttempts = 0

    """Get streams from category."""
    streams = getStreams(gameID)
    if not streams:
        print("Error. Could not get streams.")
        continue

    while streams and downloadCount < 5 and downloadAttempts < 10:

        """Get random stream."""
        stream = random.choice(list(streams))
        streams.discard(stream)

        print(f"Stream: {stream}, gameID: {gameID}")

        """Download frames from a stream, update the database."""
        download = False
        for framePath in downloadFrames(stream, gameID):
            download = True
            frameCount += 1

            """Save a frame in the database."""
            with sessionScope() as session:
                addFrame(session, framePath, gameID, stream)
        
        downloadCount += download
        downloadAttempts += 1

        downloadCountGlobal += download
        failCount += not download
            

"""Update the database."""
with sessionScope() as session:
    updateFrameCount(session)


print("Done.")
print(f"Downloaded {frameCount} frames from {downloadCountGlobal} stream(s). " + \
      f"Failed {failCount} time(s).")
