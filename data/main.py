from api import *
from dbFuncs import *

with sessionScope() as session:
    updateGames(session, getTopGames())