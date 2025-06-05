from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey 
from sqlalchemy import DateTime, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime

# Create a base class for the ORM models
Base = declarative_base()

class EggnogQuery(Base):
    pass
