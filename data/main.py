from download import *
from api import *
from dbFuncs import *

with sessionScope() as session:
    #updateGames(session, getTopGames())
    #print(minDataCategory(session))
    #addFrame(session, "/aasdfsdf/gsasdfdf/453345.png", "500188", "pokelawls")
    print


"""
for streamer in getStreamers(9618):
    print(streamer)
    downloadStream(streamer)
"""

for path in downloadFrames("vadikus007", 45345):
    print(path)