from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./crypto.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LiveNews(Base):
    __tablename__ = "live_news"  # اسم جدول جدید در دیتابیس

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    text = Column(String)
    summary = Column(String)
    url = Column(String)
    source = Column(String)
    date = Column(String)  # Store as ISO format datetime string in UTC
    sentiment = Column(String)       # جیسون خام
    sentiment_label = Column(String) # لیبل نهایی (Positive/Negative)
    sentiment_score = Column(Float)  # نمره اطمینان
    # Separate VADER sentiment fields
    vader_label = Column(String, nullable=True)
    vader_score = Column(Float, nullable=True)
    # Separate FinBERT sentiment fields
    finbert_label = Column(String, nullable=True)
    finbert_score = Column(Float, nullable=True)