
I'm using:
- Python 2.7.6 on Linux, 
- SQLAlchemy version 0.9.9.
- PostgreSQL 9.3

Thanks -
terry

Hi there,
I have been pulling my hair out on this one.

I understood that objects make it into the session only due to an explicit call to add().  But, I seem to be seeing objects being added without my explicitly doing so.  Is this to be expected ?

For instance, I want to establish a many-to-many relationship between two classes: say, for the purposes here, "Person" and "Kid".


    test=> create table persons (id SERIAL NOT NULL);
    test=> CREATE TABLE person_to_kids (person_id INT NOT NULL, kid_id INT NOT NULL);
    test=> create table kids (id SERIAL NOT NULL, name TEXT NOT NULL);
    test=> insert into  kids (name) VALUES ('Fred');
    test=> insert into  kids (name) VALUES ('Barney');

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



What is puzzling me is that, if I have a collection of Kid objects, and I assign it to the kids collection in a Person, the Person object seems to be automatically added to the session and marked as pending, even if I have not added it. 

For instance, if the Persons table is empty:

    test=> select * from persons;
     id
    ----
    (0 rows)



and I run the following code:

    print(session.new)
    obj = Person(kids = ['Barney', 'Fred'])
    print("obj has been created")
    print(session.new)
    session.commit()


The output shows that the Person object is added immediately after the assignment to obj.kids, without any call to session.add() anywhere in the code:

    IdentitySet([])
    __init__ before kids assignment
    IdentitySet([])
    After assignment to self.kids
    IdentitySet([<__main__.Person object at 0x7fb6ce447b10>])
    obj has been created
    IdentitySet([<__main__.Person object at 0x7fb6ce447b10>])


And indeed, due to the commit() at the end, the person object makes it into the database:

    test=> select * from persons;
     id
    ----
     10
    (1 row)



But, I understood that objects (only) make it into a session by virtue of being explicitly added.

So, is this the correct behavior, or am I misunderstanding something ?

If I'm not misunderstanding this all, the complete code is at https://github.com/NuggyBuggy/sqlalchemy_question.git .

Thanks for reading,
terry# sqlalchemy_question
Question to SQLalchemy group about objects being added to a session inadvertently.



