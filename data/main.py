from download import downloadFrames
from api import *
from dbFuncs import *

import threading

import random

def inputThread(inputList):
    """Thread that waits for an input."""
    input()
    print("Interrupting.")
    inputList.append(True)

"""Start a thread that updates `inputList` with inputs."""
inputList = []
threading.Thread(target=inputThread, args=(inputList, )).start()
print("Press Enter to stop downloading.")


# Update data while no input (Enter not pressed)
while not inputList:
    
    with sessionScope() as session:
        # Update top categories
        games = getTopGames()
        updateGames(session, games)
        updateFrameCount(session)

        # Get category with least data
        gameID = minDataCategory(session)

        # Update category (download frames 5 times)
        downloadCount = 0
        downloadAttempts = 0
        # Get streams from category
        streams = getStreams(gameID)
        while streams and downloadCount < 5 and downloadAttempts < 10:

            # Get random stream
            stream = streams.pop()

            print(f"Stream: {stream}, gameID: {gameID}")

            # Download frames from stream, update database
            download = False
            for framePath in downloadFrames(stream, gameID):
                download = True
                # Save frame in database
                addFrame(session, framePath, gameID, stream)
            
            downloadCount += download
            downloadAttempts += 1
        
with sessionScope() as session:
    updateFrameCount(session)

print("Completed.")
