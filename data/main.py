from download import downloadFrames
from api import *
from dbFuncs import *

import threading

import random

def inputThread(inputList):
    """
    Thread that waits for an input.
    """
    input()
    print("Interrupting.")
    inputList.append(True)

"""
Start a thread that updates `inputList` with inputs.
"""
inputList = []
threading.Thread(target=inputThread, args=(inputList, )).start()
print("Press Enter to stop downloading.")


# Update data while no input
while not inputList:
    
    with sessionScope() as session:
        # Update top categories
        games = getTopGames()
        updateGames(session, games)

        # Get category with least data
        gameID = minDataCategory(session)

        # Update category (download frames 5 times)
        # Get streams from category
        streams = getStreams(gameID)
        triedStreams = set()
        for _ in range(5):

            # Get random stream
            stream = random.choice(streams.difference(triedStreams))
            triedStreams.add(stream)

            


            # Download frames from stream, update database


print("Completed.")

# Print table contents
with sessionScope() as session:
    for query in session.query(Game).all():
        print(query)
    for query in session.query(Frame).all():
        print(query)
