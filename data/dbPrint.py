"""Print table contents for debugging."""

from dbFuncs import *

# Print table contents
with sessionScope() as session:
    #for query in session.query(Game).order_by(Game.id).all():
    #    print(query)
    for query in session.query(Frame).filter_by(game_id=490100).all():
        print(query)
