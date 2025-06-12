from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey 
from sqlalchemy import DateTime, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime

# Create a base class for the ORM models
Base = declarative_base()

class EggnogQuery(Base):
    __tablename__ = 'eggnog_query'
    
    id = Column(Integer, primary_key=True)
    query_id = Column(String, nullable=False, unique=True)
    seed_ortholog = Column(String)
    evalue = Column(Float)
    score = Column(Float)
    max_annot_lvl = Column(String)
    description = Column(Text)
    preferred_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    cog_categories = relationship("COGCategory", back_populates="query",
                                  cascade="all, delete-orphan")

class COGCategory(Base):
    __tablename__ = 'cog_category'
    
    id = Column(Integer, primary_key=True)
    query_id = Column(String,
                      ForeignKey('eggnog_query.query_id'),
                      nullable=False)
    category = Column(String, nullable=False)

    query = relationship("EggnogQuery", back_populates="cog_categories")


def init_db():
    # Add echo=True?
    engine = create_engine('postgresql://eggnog:password@localhost:5432/eggnogdb')
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()

