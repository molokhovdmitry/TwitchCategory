"""
This file will interact with a database.
"""
# Connect to postgres database
from config import DB_USER, DB_PASSWORD

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': DB_USER,
    'password': DB_PASSWORD,
    'database': 'mydb'
}


from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

engine = create_engine(URL(**DATABASE), echo=True)


from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<User(name='%s')>" % (self.name)


"""
from sqlalchemy.orm.session import Session
from config import DB_USER, DB_PASSWORD

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': DB_USER,
    'password': DB_PASSWORD,
    'database': 'mydb'
}

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

engine = create_engine(URL(**DATABASE))

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()

class Post(DeclarativeBase):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    url = Column('url', String)


from sqlalchemy.orm import sessionmaker

def main():
    engine = create_engine(URL(**DATABASE))
    DeclarativeBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    new_post = Post(name='Two record', url="http://testsite.ru/first_record")
    session.add(new_post)

    for post in session.query(Post):
        print(post)

if __name__ == "__main__":
    main()
"""