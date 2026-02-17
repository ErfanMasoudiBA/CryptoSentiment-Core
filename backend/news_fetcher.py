import requests
import datetime
import feedparser
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
# نکته مهم: LiveNews را ایمپورت کن
from database import SessionLocal, LiveNews
from ai_engine import CryptoAI

CRYPTOCOMPARE_API_URL = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
NEWS_API_URL = "https://newsapi.org/v2/everything"
COINDESK_API_URL = "https://www.coindesk.com/feed"
CRIPTONOMIST_RSS_URL = "https://cointelegraph.com/rss"  # We'll need to handle RSS

# You'll need to get a free API key from https://newsapi.org/
NEWS_API_KEY = "YOUR_NEWS_API_KEY_HERE"  # Replace with actual API key or make it configurable

def fetch_cryptocompare_news(limit=5):
    """Fetch news from CryptoCompare API"""
    try:
        response = requests.get(CRYPTOCOMPARE_API_URL)
        data = response.json()
        articles = []
        for item in data.get('Data', [])[:limit]:
            articles.append({
                'title': item.get('title', ''),
                'body': item.get('body', ''),
                'url': item.get('url', ''),
                'source': item.get('source_info', {}).get('name', 'CryptoCompare'),
                'published_on': item.get('published_on', 0),
                'image_url': item.get('imageurl', '')
            })
        return articles
    except Exception as e:
        print(f"Error fetching from CryptoCompare: {e}")
        return []

def fetch_newsapi_articles(limit=5):
    """Fetch crypto-related news from NewsAPI"""
    if NEWS_API_KEY == "YOUR_NEWS_API_KEY_HERE":
        print("⚠️ NewsAPI key not configured, skipping NewsAPI fetch")
        return []
    
    try:
        params = {
            'q': 'cryptocurrency OR bitcoin OR ethereum',
            'sortBy': 'publishedAt',
            'pageSize': limit,
            'apiKey': NEWS_API_KEY
        }
        response = requests.get(NEWS_API_URL, params=params)
        data = response.json()
        articles = []
        for item in data.get('articles', [])[:limit]:
            published_at = item.get('publishedAt', '')
            # Convert ISO format to timestamp
            if published_at:
                dt = datetime.datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                timestamp = int(dt.timestamp())
            else:
                timestamp = int(datetime.datetime.now().timestamp())
            
            articles.append({
                'title': item.get('title', ''),
                'body': item.get('description', '') or item.get('content', ''),
                'url': item.get('url', ''),
                'source': item.get('source', {}).get('name', 'NewsAPI'),
                'published_on': timestamp,
                'image_url': item.get('urlToImage', '')
            })
        return articles
    except Exception as e:
        print(f"Error fetching from NewsAPI: {e}")
        return []

def fetch_coindesk_news(limit=5):
    """Fetch news from CoinDesk RSS feed"""
    try:
        rss_url = "https://www.coindesk.com/feed/"
        feed = feedparser.parse(rss_url)
        articles = []
        for entry in feed.entries[:limit]:
            # Parse publication date
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_dt = datetime.datetime(*entry.published_parsed[:6])
                timestamp = int(published_dt.timestamp())
            else:
                timestamp = int(datetime.datetime.now().timestamp())
            
            # Get content from description or content
            content = getattr(entry, 'summary', '')
            if not content and hasattr(entry, 'content'):
                content = entry.content[0].value if entry.content else ''
            
            articles.append({
                'title': entry.get('title', ''),
                'body': content,
                'url': entry.get('link', ''),
                'source': 'CoinDesk',
                'published_on': timestamp,
                'image_url': ''  # Extract from content if available
            })
        return articles
    except Exception as e:
        print(f"Error fetching from CoinDesk: {e}")
        return []

def fetch_cointelegraph_news(limit=5):
    """Fetch news from CoinTelegraph RSS feed"""
    try:
        rss_url = "https://cointelegraph.com/rss"
        feed = feedparser.parse(rss_url)
        articles = []
        for entry in feed.entries[:limit]:
            # Parse publication date
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_dt = datetime.datetime(*entry.published_parsed[:6])
                timestamp = int(published_dt.timestamp())
            else:
                timestamp = int(datetime.datetime.now().timestamp())
            
            # Get content from description
            content = getattr(entry, 'summary', '')
            
            articles.append({
                'title': entry.get('title', ''),
                'body': content,
                'url': entry.get('link', ''),
                'source': 'CoinTelegraph',
                'published_on': timestamp,
                'image_url': ''  # Extract from content if available
            })
        return articles
    except Exception as e:
        print(f"Error fetching from CoinTelegraph: {e}")
        return []

def fetch_crypto_news_org(limit=5):
    """Fetch news from CryptoNews.org RSS feed"""
    try:
        rss_url = "https://cryptonews.com/news/bitcoin.rss"
        feed = feedparser.parse(rss_url)
        articles = []
        for entry in feed.entries[:limit]:
            # Parse publication date
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_dt = datetime.datetime(*entry.published_parsed[:6])
                timestamp = int(published_dt.timestamp())
            else:
                timestamp = int(datetime.datetime.now().timestamp())
            
            # Get content from description
            content = getattr(entry, 'summary', '')
            
            articles.append({
                'title': entry.get('title', ''),
                'body': content,
                'url': entry.get('link', ''),
                'source': 'CryptoNews',
                'published_on': timestamp,
                'image_url': ''
            })
        return articles
    except Exception as e:
        print(f"Error fetching from CryptoNews: {e}")
        return []

def fetch_bitcoin_magazine_news(limit=5):
    """Fetch news from Bitcoin Magazine RSS feed"""
    try:
        rss_url = "https://bitcoinmagazine.com/feed"
        feed = feedparser.parse(rss_url)
        articles = []
        for entry in feed.entries[:limit]:
            # Parse publication date
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_dt = datetime.datetime(*entry.published_parsed[:6])
                timestamp = int(published_dt.timestamp())
            else:
                timestamp = int(datetime.datetime.now().timestamp())
            
            # Get content from description
            content = getattr(entry, 'summary', '')
            
            articles.append({
                'title': entry.get('title', ''),
                'body': content,
                'url': entry.get('link', ''),
                'source': 'Bitcoin Magazine',
                'published_on': timestamp,
                'image_url': ''
            })
        return articles
    except Exception as e:
        print(f"Error fetching from Bitcoin Magazine: {e}")
        return []

def fetch_crypto_slate_news(limit=5):
    """Fetch news from CryptoSlate RSS feed"""
    try:
        rss_url = "https://cryptoslate.com/feed/"
        feed = feedparser.parse(rss_url)
        articles = []
        for entry in feed.entries[:limit]:
            # Parse publication date
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_dt = datetime.datetime(*entry.published_parsed[:6])
                timestamp = int(published_dt.timestamp())
            else:
                timestamp = int(datetime.datetime.now().timestamp())
            
            # Get content from description
            content = getattr(entry, 'summary', '')
            
            articles.append({
                'title': entry.get('title', ''),
                'body': content,
                'url': entry.get('link', ''),
                'source': 'CryptoSlate',
                'published_on': timestamp,
                'image_url': ''
            })
        return articles
    except Exception as e:
        print(f"Error fetching from CryptoSlate: {e}")
        return []

def fetch_and_analyze_latest_news(limit=10):
    print(f"🌍 Connecting to Multiple Crypto News Sources (Limit: {limit})...")
    
    # Fetch from multiple sources
    all_articles = []
    
    # Fetch from CryptoCompare
    cc_articles = fetch_cryptocompare_news(limit)
    all_articles.extend(cc_articles)
    print(f"📥 Fetched {len(cc_articles)} articles from CryptoCompare")
    
    # Fetch from NewsAPI
    na_articles = fetch_newsapi_articles(limit)
    if na_articles:
        all_articles.extend(na_articles)
        print(f"📥 Fetched {len(na_articles)} articles from NewsAPI")
    
    # Fetch from CoinDesk
    cd_articles = fetch_coindesk_news(limit)
    if cd_articles:
        all_articles.extend(cd_articles)
        print(f"📥 Fetched {len(cd_articles)} articles from CoinDesk")
    
    # Fetch from CoinTelegraph
    ct_articles = fetch_cointelegraph_news(limit)
    if ct_articles:
        all_articles.extend(ct_articles)
        print(f"📥 Fetched {len(ct_articles)} articles from CoinTelegraph")
    
    # Fetch from CryptoNews
    cn_articles = fetch_crypto_news_org(limit)
    if cn_articles:
        all_articles.extend(cn_articles)
        print(f"📥 Fetched {len(cn_articles)} articles from CryptoNews")
    
    # Fetch from Bitcoin Magazine
    bm_articles = fetch_bitcoin_magazine_news(limit)
    if bm_articles:
        all_articles.extend(bm_articles)
        print(f"📥 Fetched {len(bm_articles)} articles from Bitcoin Magazine")
    
    # Fetch from CryptoSlate
    cs_articles = fetch_crypto_slate_news(limit)
    if cs_articles:
        all_articles.extend(cs_articles)
        print(f"📥 Fetched {len(cs_articles)} articles from CryptoSlate")
    
    if not all_articles:
        return {"status": "error", "message": "No articles fetched from any source"}

    print("🧠 Loading AI Engine...")
    ai = CryptoAI()
    
    db: Session = SessionLocal()
    new_count = 0
    
    print("🔄 Processing Live News...")
    for article in all_articles:
        try:
            title = article.get('title', '')
            body = article.get('body', '')
            url = article.get('url', '')
            source = article.get('source', 'Unknown')
            published_on = article.get('published_on', 0)
            
            # Handle timestamp conversion
            if isinstance(published_on, int) and published_on > 0:
                date_str = datetime.datetime.fromtimestamp(published_on).strftime('%Y-%m-%d %H:%M:%S')
            else:
                date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # چک تکراری بودن در جدول LiveNews
            exists = db.query(LiveNews).filter(LiveNews.url == url).first()
            if exists:
                continue

            full_text = f"{title}. {body}"
            
            # تحلیل با FinBERT
            finbert_res = ai.analyze_finbert(full_text)
            # تحلیل با VADER
            vader_res = ai.analyze_vader(full_text)
            
            # ذخیره در جدول جدید LiveNews
            new_item = LiveNews(
                title=title,
                text=body,
                summary=full_text[:200],
                url=url,
                source=source,
                date=date_str,
                sentiment=str({"class": finbert_res['label'], "score": finbert_res['score']}),
                sentiment_label=finbert_res['label'],
                sentiment_score=finbert_res['score'],
                vader_label=vader_res['label'],
                vader_score=vader_res['score'],
                finbert_label=finbert_res['label'],
                finbert_score=finbert_res['score']
            )
            
            db.add(new_item)
            new_count += 1
            print(f"✅ Live News Saved: {title[:30]}... [{finbert_res['label']}] from {source}")
            
        except Exception as e:
            print(f"⚠️ Error processing article: {e}")
            continue

    db.commit()
    db.close()
    return {"status": "success", "added": new_count}