from sqlalchemy import Column, Integer, String, Float
from database import Base


class News(Base):
    """News model for storing cryptocurrency news articles"""
    
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    summary = Column(String)  # Maps to 'text' from CSV
    source = Column(String)
    url = Column(String)
    published_date = Column(String)
    sentiment_label = Column(String)
    sentiment_score = Column(Float)

