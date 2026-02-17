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
    published_date = Column(String)  # Store as ISO format datetime string in UTC
    # Original sentiment fields (keeping for compatibility)
    sentiment_label = Column(String)
    sentiment_score = Column(Float)
    # Separate VADER sentiment fields
    vader_label = Column(String, nullable=True)
    vader_score = Column(Float, nullable=True)
    # Separate FinBERT sentiment fields
    finbert_label = Column(String, nullable=True)
    finbert_score = Column(Float, nullable=True)

