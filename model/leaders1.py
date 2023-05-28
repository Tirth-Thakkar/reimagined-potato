import json
import datetime
from __init__ import app, db
from sqlalchemy.exc import IntegrityError

class Leader(db.Model):
    __tablename__ = 'Leaderboard'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _score = db.Column(db.Integer, unique=False, nullable=False)
    _locations = db.Column(db.JSON, unique=False, nullable=False)
    _tot_distance = db.Column(db.Integer, unique=False, nullable=False)
    _date = db.Column(db.DateTime, default=datetime.datetime.utcnow, unique=False, nullable=False)


    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, score, locations, tot_distance, date):
        self._name = name    # variables with self prefix become part of the object, 
        self._score = score
        self._locations = locations
        self._tot_distance = tot_distance
        self._date = date


    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def score(self):
        return self._score
    
    # a setter function, allows name to be updated after initial object creation
    @score.setter
    def score(self, score):
        self._score = score
    
    # a getter method, extracts email from object
    @property
    def locations(self):
        return self._locations
    
    # a setter function, allows name to be updated after initial object creation
    @score.setter
    def locations(self, locations):
        self._locations = locations

    # a getter method, extracts email from object
    @property
    def tot_distance(self):
        return self._tot_distance
    
    # a setter function, allows name to be updated after initial object creation
    @score.setter
    def tot_distance(self, tot_distance):
        self._tot_distance = tot_distance
    
    # a getter method, extracts email from object
    @property
    def date(self):
        return self._date
    
    # a setter function, allows name to be updated after initial object creation
    @score.setter
    def date(self, date):
        self._date = date
    
   
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "name": self.name,
            "score": self.score,
            "locations": self.locations,
            "tot_distance": self.tot_distance,
            "data": self.date,
            
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", score=0,locations="",tot_distance=0,date=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if score > 0:
            self.score = score
        if len(locations) > 0:
            self.score = score
        if tot_distance > 0:
            self.score = score
        if len(date) > 0:
            self.score = score
        
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


def initLeaders():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        score1 = Leader(name='Chester', score = 100)
        score2 = Leader(name='Sonic Hedgehog', score = 15)
        score3 = Leader(name='Megamind', score = 3)
        score4 = Leader(name='Gamer Man', score = 215)

        leaders = [score1, score2, score3, score4]

        for leader in leaders:
            try:
                leader.create()
            except IntegrityError:
                db.session.remove()
                print(f"error try again later")
            