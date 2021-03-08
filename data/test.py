from download import downloadFrames
from api import *
from dbFuncs import *


for path in downloadFrames("nymn", 76457):
    print(path)

"""
def a(k):
    for i in range(5):
        if k == 0:
            print("a")
            return None
        yield i

for b in a(0):
    print(b)
"""