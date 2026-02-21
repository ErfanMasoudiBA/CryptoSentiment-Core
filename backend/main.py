import pandas as pd
import ast
import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base, LiveNews
from models import News
from ai_engine import CryptoAI
from sqlalchemy import text

# ساخت جداول دیتابیس اگر وجود ندارند
# Update existing tables with new columns if needed
Base.metadata.create_all(bind=engine)

# Add new columns if they don't exist
try:
    with engine.connect() as conn:
        # Check if VADER and FinBERT columns exist in news table, if not create them
        try:
            conn.execute(text("ALTER TABLE news ADD COLUMN vader_label TEXT DEFAULT 'neutral'"))
        except:
            pass  # Column already exists
        try:
            conn.execute(text("ALTER TABLE news ADD COLUMN vader_score REAL DEFAULT 0.0"))
        except:
            pass  # Column already exists
        try:
            conn.execute(text("ALTER TABLE news ADD COLUMN finbert_label TEXT DEFAULT 'neutral'"))
        except:
            pass  # Column already exists
        try:
            conn.execute(text("ALTER TABLE news ADD COLUMN finbert_score REAL DEFAULT 0.0"))
        except:
            pass  # Column already exists
            
        # Check if VADER and FinBERT columns exist in live_news table, if not create them
        try:
            conn.execute(text("ALTER TABLE live_news ADD COLUMN vader_label TEXT DEFAULT 'neutral'"))
        except:
            pass  # Column already exists
        try:
            conn.execute(text("ALTER TABLE live_news ADD COLUMN vader_score REAL DEFAULT 0.0"))
        except:
            pass  # Column already exists
        try:
            conn.execute(text("ALTER TABLE live_news ADD COLUMN finbert_label TEXT DEFAULT 'neutral'"))
        except:
            pass  # Column already exists
        try:
            conn.execute(text("ALTER TABLE live_news ADD COLUMN finbert_score REAL DEFAULT 0.0"))
        except:
            pass  # Column already exists
            
        conn.commit()
except Exception as e:
    # Handle any other database errors
    print(f"Schema update completed or error: {e}")

app = FastAPI(title="CryptoSentiment Core")

# AI engine instance (initialized at startup)
ai_engine: CryptoAI = None

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
    try:
        if db.query(News).count() > 0:
            print("Database already has data. Skipping seed.")
            return
    except Exception as e:
        print(f"Error checking database: {e}")
        # If there's an error (like missing columns), we'll continue with seeding
        # The create_all will handle schema updates
        pass

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
    global ai_engine
    db = SessionLocal()
    seed_database(db)
    db.close()
    ai_engine = CryptoAI()

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"status": "Online", "project": "CryptoSentiment-Core"}

# 1. گرفتن لیست اخبار (با قابلیت صفحه‌بندی)
@app.get("/api/news")
def get_news(skip: int = 0, limit: int = 50, q: str = None, start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    query = db.query(News)
    
    if q:
        # Filter by coin name in title or summary
        query = query.filter(
            News.title.contains(q) | 
            News.summary.contains(q)
        )
        
    # Filter by date range if provided
    if start_date:
        # Convert to datetime format for proper comparison
        query = query.filter(News.published_date >= f"{start_date} 00:00:00")
    if end_date:
        # Convert to datetime format for proper comparison
        query = query.filter(News.published_date <= f"{end_date} 23:59:59")
        
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

# 2a. گرفتن آمار VADER
@app.get("/api/vader_stats")
def get_vader_stats(q: str = None, start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    query = db.query(News)
    
    if q:
        # Filter by coin name in title or summary
        query = query.filter(
            News.title.contains(q) | 
            News.summary.contains(q)
        )
        
    # Filter by date range if provided
    if start_date:
        # Convert to datetime format for proper comparison
        query = query.filter(News.published_date >= f"{start_date} 00:00:00")
    if end_date:
        # Convert to datetime format for proper comparison
        query = query.filter(News.published_date <= f"{end_date} 23:59:59")
        
    total = query.count()
    positive = query.filter(News.vader_label == 'positive').count()
    negative = query.filter(News.vader_label == 'negative').count()
    neutral = query.filter(News.vader_label == 'neutral').count()
    
    return {
        "total": total,
        "positive": positive,
        "negative": negative,
        "neutral": neutral
    }

# 2b. گرفتن آمار FinBERT
@app.get("/api/finbert_stats")
def get_finbert_stats(q: str = None, start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    query = db.query(News)
    
    if q:
        # Filter by coin name in title or summary
        query = query.filter(
            News.title.contains(q) | 
            News.summary.contains(q)
        )
        
    # Filter by date range if provided
    if start_date:
        # Convert to datetime format for proper comparison
        query = query.filter(News.published_date >= f"{start_date} 00:00:00")
    if end_date:
        # Convert to datetime format for proper comparison
        query = query.filter(News.published_date <= f"{end_date} 23:59:59")
        
    total = query.count()
    positive = query.filter(News.finbert_label == 'positive').count()
    negative = query.filter(News.finbert_label == 'negative').count()
    neutral = query.filter(News.finbert_label == 'neutral').count()
    
    return {
        "total": total,
        "positive": positive,
        "negative": negative,
        "neutral": neutral
    }


# --- Request models for AI endpoints ---
class AnalyzeTextRequest(BaseModel):
    text: str
    model: str  # "vader" or "finbert"


class ReanalyzeDbRequest(BaseModel):
    model: str  # "vader" or "finbert"
    limit: int = 100


# 3. Live AI Playground: analyze text with VADER or FinBERT
@app.post("/api/analyze_text")
def analyze_text(body: AnalyzeTextRequest):
    if ai_engine is None:
        raise HTTPException(status_code=503, detail="AI engine not initialized")
    model = body.model.strip().lower()
    if model not in ("vader", "finbert"):
        raise HTTPException(status_code=400, detail="model must be 'vader' or 'finbert'")
    if model == "vader":
        result = ai_engine.analyze_vader(body.text)
    else:
        result = ai_engine.analyze_finbert(body.text)
    return result


# 4. Re-analyze news in DB with selected model
@app.post("/api/reanalyze_db")
def reanalyze_db(body: ReanalyzeDbRequest, db: Session = Depends(get_db)):
    if ai_engine is None:
        raise HTTPException(status_code=503, detail="AI engine not initialized")
    model = body.model.strip().lower()
    if model not in ("vader", "finbert"):
        raise HTTPException(status_code=400, detail="model must be 'vader' or 'finbert'")
    limit = max(1, min(body.limit, 1000))  # clamp 1..1000 for speed/safety

    rows = db.query(News).order_by(News.id).limit(limit).all()
    for row in rows:
        text = f"{row.title or ''} {row.summary or ''}".strip()
        if not text:
            continue
        if model == "vader":
            result = ai_engine.analyze_vader(text)
        else:
            result = ai_engine.analyze_finbert(text)
        row.sentiment_label = result.get("label", "neutral")
        row.sentiment_score = float(result.get("score", 0.0))
    db.commit()
    return {"status": "success", "updated_count": len(rows)}

# اندپوینت جدید برای گرفتن لیست اخبار زنده
@app.get("/api/live_news")
def get_live_news_list(start_date: str = None, end_date: str = None, limit: int = 20, db: Session = Depends(get_db)):
    query = db.query(LiveNews)
    
    # Filter by date range if provided
    if start_date:
        # Convert to datetime format for proper comparison
        query = query.filter(LiveNews.date >= f"{start_date} 00:00:00")
    if end_date:
        # Convert to datetime format for proper comparison
        query = query.filter(LiveNews.date <= f"{end_date} 23:59:59")
    
    # جدیدترین‌ها اول بیان (desc)
    news = query.order_by(LiveNews.id.desc()).limit(limit).all()
    return news

# API endpoints for VADER and FinBERT stats for live news
@app.get("/api/live_vader_stats")
def get_live_vader_stats(start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    query = db.query(LiveNews)
    
    # Filter by date range if provided
    if start_date:
        # Convert to datetime format for proper comparison
        query = query.filter(LiveNews.date >= f"{start_date} 00:00:00")
    if end_date:
        # Convert to datetime format for proper comparison
        query = query.filter(LiveNews.date <= f"{end_date} 23:59:59")
        
    total = query.count()
    positive = query.filter(LiveNews.vader_label == 'positive').count()
    negative = query.filter(LiveNews.vader_label == 'negative').count()
    neutral = query.filter(LiveNews.vader_label == 'neutral').count()
    
    return {
        "total": total,
        "positive": positive,
        "negative": negative,
        "neutral": neutral
    }

@app.get("/api/live_finbert_stats")
def get_live_finbert_stats(start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    query = db.query(LiveNews)
    
    # Filter by date range if provided
    if start_date:
        # Convert to datetime format for proper comparison
        query = query.filter(LiveNews.date >= f"{start_date} 00:00:00")
    if end_date:
        # Convert to datetime format for proper comparison
        query = query.filter(LiveNews.date <= f"{end_date} 23:59:59")
        
    total = query.count()
    positive = query.filter(LiveNews.finbert_label == 'positive').count()
    negative = query.filter(LiveNews.finbert_label == 'negative').count()
    neutral = query.filter(LiveNews.finbert_label == 'neutral').count()
    
    return {
        "total": total,
        "positive": positive,
        "negative": negative,
        "neutral": neutral
    }

@app.post("/api/fetch_live_news")
def trigger_live_news_fetch(limit: int = 5):
    from news_fetcher import fetch_and_analyze_latest_news
    result = fetch_and_analyze_latest_news(limit=limit)
    return result
