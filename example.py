import logging
iteration = 1
logging.basicConfig(level=logging.DEBUG)

from sqlalchemy import create_engine, Column, Integer, Boolean,\
    String, Sequence, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
global engine
engine = create_engine('postgresql://test_user:test@localhost:5432/test')

Session = sessionmaker(bind=engine)
global session
session = Session()



""" Establish a many-to-many relation between Person and Kids  """

person_to_kids = Table('person_to_kids',
                        Base.metadata,
                        Column('person_id', Integer, ForeignKey('persons.id')),
                        Column('kid_id', Integer, ForeignKey('kids.id')))
class Person(Base):

    __tablename__ = 'persons'
    id = Column('id', Integer, primary_key = True)
    def __init__(self,
                 kids = []):

        kids = Kid.get_kids(kid_names = kids)

        print("__init__ before kids assignment")
        print(session.new)

        """ Assigning to self.kids here seems to add self to session ??? """

        self.kids=kids
        print("After assignment to self.kids")
        print(session.new)


class Kid(Base):
    __tablename__ = 'kids'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    parents = relationship("Person",
                               secondary = person_to_kids,
                               backref="kids")

    def __init__(self, name = None):
        self.name = name

    @staticmethod
    def get_kids(kid_names = []):

        kids = []

        for name in kid_names:
            # find first kid
            target_set = session.query(Kid).filter(Kid.name == name).first()
            kids.append(target_set)

        return kids

print(session.new)
obj = Person(kids = ['Barney', 'Fred'])
print("obj has been created")
print(session.new)
session.commit()

