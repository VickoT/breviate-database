from sqlalchemy import Column, Integer, Float, String, Text, ForeignKey 
from sqlalchemy import DateTime, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime

# Create a base class for the ORM models
Base = declarative_base()

class EggnogQuery(Base):
    __tablename__ = 'eggnog_query'

    # I should remove id, query_id is unique
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
    query_id = Column(String, ForeignKey('eggnog_query.query_id'), nullable=False)
    category = Column(String, ForeignKey('cog_category_description.category'), nullable=False)

    query = relationship("EggnogQuery", back_populates="cog_categories")
    description_entry = relationship("COGCategoryDescription",
                                     back_populates="cog_entries",
                                     foreign_keys=[category])


class COGCategoryDescription(Base):
    __tablename__ = 'cog_category_description'
    
    category = Column(String, primary_key=True)
    description = Column(Text, nullable=False)

    cog_entries = relationship("COGCategory", back_populates="description_entry")


def init_db():
    # Add echo=True?
    engine = create_engine('postgresql://eggnog:password@localhost:5432/eggnogdb')
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()

