from download import downloadFrames
from api import *
from dbFuncs import *


"""
with sessionScope() as session:
    updateFrameCount(session)
    for game in session.query(Game).all():
        print(game)
"""




"""
for path in downloadFrames("nymn", 76457):
    print(path)
"""


def a(k):
    for i in range(5):
        if k == 0:
            print("a")
            return None
        yield i

c = False
for b in a(1):
    c = True
    print(b)
print(c)