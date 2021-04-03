from data.db import Frame
from data.dbFuncs import syncDB, sessionScope

def sync():
    with sessionScope() as session:
        before = len(session.query(Frame).all())
        syncDB(session)
        after = len(session.query(Frame).all())
        deleted = before - after

    print(f"Deleted {deleted} frames from the database.")


if __name__ == "__main__":
    sync()
