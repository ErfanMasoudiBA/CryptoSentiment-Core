import pandas as pd
import ast
import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import News

# ساخت جداول دیتابیس اگر وجود ندارند
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CryptoSentiment Core")

# تنظیمات دسترسی (CORS) برای فلاتر و Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تابع اتصال به دیتابیس
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- تابع کلیدی: انتقال دیتا از CSV به دیتابیس ---
def seed_database(db: Session):
    # چک می‌کنیم اگر دیتابیس خالی است، پرش کنیم
    if db.query(News).count() > 0:
        print("Database already has data. Skipping seed.")
        return

    print("Seeding database from CSV...")
    csv_path = os.path.join("data", "cryptonews.csv")
    
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return

    # خواندن فایل
    df = pd.read_csv(csv_path)
    # Loading all rows from the CSV file

    news_to_add = []
    for _, row in df.iterrows():
        # استخراج لیبل احساسات از فرمت خاص رشته‌ای
        try:
            # تبدیل "{'class': 'negative', ...}" به دیکشنری
            sent_dict = ast.literal_eval(row['sentiment'])
            label = sent_dict.get('class', 'neutral')
            score = float(sent_dict.get('polarity', 0.0))
        except:
            label = 'neutral'
            score = 0.0

        news_item = News(
            title=str(row['title']),
            summary=str(row['text']),  # ستون text در csv میره توی summary
            source=str(row['source']),
            url=str(row['url']),
            published_date=str(row['date']),
            sentiment_label=label,
            sentiment_score=score
        )
        news_to_add.append(news_item)
    
    db.add_all(news_to_add)
    db.commit()
    print(f"Successfully added {len(news_to_add)} news items to database.")

# اجرای تابع سیدینگ در لحظه بالا آمدن برنامه
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    seed_database(db)
    db.close()

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"status": "Online", "project": "CryptoSentiment-Core"}

# 1. گرفتن لیست اخبار (با قابلیت صفحه‌بندی)
@app.get("/api/news")
def get_news(skip: int = 0, limit: int = 50, q: str = None, db: Session = Depends(get_db)):
    query = db.query(News)
    
    if q:
        # Filter by coin name in title or summary
        query = query.filter(
            News.title.contains(q) | 
            News.summary.contains(q)
        )
    
    news = query.offset(skip).limit(limit).all()
    return news

# 2. گرفتن آمار برای نمودارها
@app.get("/api/stats")
def get_stats(q: str = None, db: Session = Depends(get_db)):
    query = db.query(News)
    
    if q:
        # Filter by coin name in title or summary
        query = query.filter(
            News.title.contains(q) | 
            News.summary.contains(q)
        )
    
    total = query.count()
    positive = query.filter(News.sentiment_label == 'positive').count()
    negative = query.filter(News.sentiment_label == 'negative').count()
    neutral = query.filter(News.sentiment_label == 'neutral').count()
    
    return {
        "total": total,
        "positive": positive,
        "negative": negative,
        "neutral": neutral
    }