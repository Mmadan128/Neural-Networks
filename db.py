# db.py
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL (update it according to your setup)
DATABASE_URL = 'sqlite:///your_database.db'  # Use your actual database URI

# Create the engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Base class for our models
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String)

# Define the Event model
class Event(Base):
    __tablename__ = 'events'
    event_id = Column(Integer, primary_key=True)
    title = Column(String)
    music = Column(Integer)
    sports = Column(Integer)
    comedy = Column(Integer)
    art = Column(Integer)
    tech = Column(Integer)
    theater = Column(Integer)
    dance = Column(Integer)

# Define the UserEventInteraction model
class UserEventInteraction(Base):
    __tablename__ = 'user_event_interactions'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    event_id = Column(Integer, ForeignKey('events.event_id'), primary_key=True)
    rating = Column(Float)  # Or any other interaction metric

# Create tables if they don’t already exist
Base.metadata.create_all(engine)
