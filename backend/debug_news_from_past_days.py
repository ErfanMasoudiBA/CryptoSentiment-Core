import datetime
from datetime import date, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal, LiveNews
from models import News

def get_most_recent_news(limit=20):
    """
    Fetch the most recent news items regardless of date
    """
    print("=== FETCHING MOST RECENT NEWS ITEMS ===")
    
    # Create database session
    db: Session = SessionLocal()
    
    try:
        # Get most recent live news
        print("\n--- LATEST LIVE NEWS ANALYSIS ---")
        live_news = db.query(LiveNews).order_by(LiveNews.id.desc()).limit(limit).all()
        
        if live_news:
            print(f"Found {len(live_news)} recent live news articles:")
            for i, news in enumerate(live_news, 1):
                print(f"\n{i}. Title: {news.title[:100]}...")
                print(f"   Source: {news.source}")
                print(f"   Date: {news.date}")
                print(f"   VADER Analysis - Label: {news.vader_label}, Score: {news.vader_score:.3f}")
                print(f"   FinBERT Analysis - Label: {news.finbert_label}, Score: {news.finbert_score:.3f}")
                print(f"   URL: {news.url}")
        else:
            print("No live news found in database")
        
        # Also get most recent original news
        print("\n--- LATEST ORIGINAL NEWS ANALYSIS ---")
        original_news = db.query(News).order_by(News.id.desc()).limit(limit).all()
        
        if original_news:
            print(f"Found {len(original_news)} recent original news articles:")
            for i, news in enumerate(original_news, 1):
                print(f"\n{i}. Title: {news.title[:100]}...")
                print(f"   Source: {news.source}")
                print(f"   Date: {news.published_date}")
                print(f"   Original Sentiment Label: {news.sentiment_label}")
                print(f"   Original Sentiment Score: {news.sentiment_score:.3f}")
                # Check if VADER and FinBERT fields exist and are populated
                try:
                    if hasattr(news, 'vader_label') and news.vader_label:
                        print(f"   VADER Analysis - Label: {news.vader_label}, Score: {news.vader_score:.3f}")
                    else:
                        print("   VADER Analysis - Label: Not analyzed, Score: N/A")
                        
                    if hasattr(news, 'finbert_label') and news.finbert_label:
                        print(f"   FinBERT Analysis - Label: {news.finbert_label}, Score: {news.finbert_score:.3f}")
                    else:
                        print("   FinBERT Analysis - Label: Not analyzed, Score: N/A")
                except AttributeError:
                    print("   VADER/FinBERT analysis not available for this record")
                print(f"   URL: {news.url}")
        else:
            print("No original news found in database")
            
    except Exception as e:
        print(f"Error querying database: {e}")
    finally:
        db.close()

def get_news_from_past_days(days_ago=7, limit=20):
    """
    Fetch news from a specific number of days ago
    """
    # Calculate the date from N days ago
    target_date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime('%Y-%m-%d')
    print(f"Fetching news from {days_ago} days ago (date: {target_date})...")
    
    # Create database session
    db: Session = SessionLocal()
    
    try:
        # Query for news from the specific date
        # We'll look for records where the date matches the target date
        # The date format in the database might vary, so we'll handle different formats
        
        # First, let's try to fetch from LiveNews table (newer live news)
        print("\n=== LIVE NEWS ANALYSIS ===")
        live_news = db.query(LiveNews).filter(
            LiveNews.date.like(f'{target_date}%')  # Match date at the beginning
        ).limit(limit).all()
        
        if live_news:
            print(f"Found {len(live_news)} live news articles from {target_date}:")
            for i, news in enumerate(live_news, 1):
                print(f"\n{i}. Title: {news.title[:100]}...")
                print(f"   Source: {news.source}")
                print(f"   Date: {news.date}")
                print(f"   VADER Analysis - Label: {news.vader_label}, Score: {news.vader_score:.3f}")
                print(f"   FinBERT Analysis - Label: {news.finbert_label}, Score: {news.finbert_score:.3f}")
                print(f"   URL: {news.url}")
        else:
            print(f"No live news found from {target_date}")
        
        # Also try to fetch from the original News table (seeded data)
        print("\n=== ORIGINAL NEWS ANALYSIS ===")
        original_news = db.query(News).filter(
            News.published_date.like(f'{target_date}%')  # Match date at the beginning
        ).limit(limit).all()
        
        if original_news:
            print(f"Found {len(original_news)} original news articles from {target_date}:")
            for i, news in enumerate(original_news, 1):
                print(f"\n{i}. Title: {news.title[:100]}...")
                print(f"   Source: {news.source}")
                print(f"   Date: {news.published_date}")
                print(f"   Sentiment Label: {news.sentiment_label}")
                print(f"   Sentiment Score: {news.sentiment_score:.3f}")
                # Note: VADER and FinBERT fields might not be populated in original news
                try:
                    print(f"   VADER Analysis - Label: {news.vader_label}, Score: {news.vader_score:.3f}")
                    print(f"   FinBERT Analysis - Label: {news.finbert_label}, Score: {news.finbert_score:.3f}")
                except AttributeError:
                    print("   VADER/FinBERT analysis not available for this record")
                print(f"   URL: {news.url}")
        else:
            print(f"No original news found from {target_date}")
            
    except Exception as e:
        print(f"Error querying database: {e}")
    finally:
        db.close()

def get_news_by_relative_date(days_ago=7, limit=20):
    """
    Alternative approach to get news from approximately N days ago
    """
    print(f"\n=== ALTERNATIVE SEARCH FOR NEWS FROM APPROXIMATELY {days_ago} DAYS AGO ===")
    
    db: Session = SessionLocal()
    
    try:
        # Get the date N days ago
        target_date = datetime.date.today() - datetime.timedelta(days=days_ago)
        print(f"Target date: {target_date}")
        
        # Try to get news from LiveNews table
        live_news = db.query(LiveNews).filter(
            # Extract just the date part for comparison
            LiveNews.date.like(f'{target_date.strftime("%Y-%m-%d")}%')
        ).limit(limit).all()
        
        if live_news:
            print(f"Found {len(live_news)} live news items:")
            for i, news in enumerate(live_news, 1):
                # Parse the date to confirm it's from the right day
                news_date_str = news.date.split()[0] if ' ' in news.date else news.date
                print(f"\n{i}. [{news_date_str}] {news.title[:80]}...")
                print(f"   Source: {news.source}")
                print(f"   VADER: {news.vader_label} ({news.vader_score:.3f})")
                print(f"   FinBERT: {news.finbert_label} ({news.finbert_score:.3f})")
        else:
            print("No live news found for this date.")
            
        # Also try for original news
        original_news = db.query(News).filter(
            # Extract just the date part for comparison
            News.published_date.like(f'{target_date.strftime("%Y-%m-%d")}%')
        ).limit(limit).all()
        
        if original_news:
            print(f"\nFound {len(original_news)} original news items:")
            for i, news in enumerate(original_news, 1):
                news_date_str = news.published_date.split()[0] if ' ' in news.published_date else news.published_date
                print(f"\n{i}. [{news_date_str}] {news.title[:80]}...")
                print(f"   Source: {news.source}")
                print(f"   Original Sentiment: {news.sentiment_label} ({news.sentiment_score:.3f})")
                try:
                    print(f"   VADER: {news.vader_label} ({news.vader_score:.3f})")
                    print(f"   FinBERT: {news.finbert_label} ({news.finbert_score:.3f})")
                except AttributeError:
                    print("   VADER/FinBERT analysis: Not available")
        else:
            print("No original news found for this date.")
            
    except Exception as e:
        print(f"Error in alternative search: {e}")
    finally:
        db.close()

def list_recent_dates():
    """
    Helper function to see what dates are available in the database
    """
    print("\n=== AVAILABLE DATES IN DATABASE ===")
    
    db: Session = SessionLocal()
    
    try:
        # Get unique dates from LiveNews
        live_dates = db.query(LiveNews.date).distinct().limit(10).all()
        if live_dates:
            print("Recent dates in LiveNews table:")
            # Extract and group by date part
            date_counts = {}
            for date_record in live_dates:
                date_part = date_record[0].split()[0] if ' ' in date_record[0] else date_record[0]
                date_counts[date_part] = date_counts.get(date_part, 0) + 1
            
            for date_str in sorted(date_counts.keys(), reverse=True)[:10]:
                print(f"  {date_str}: {date_counts[date_str]} entries")
        
        # Get unique dates from News
        original_dates = db.query(News.published_date).distinct().limit(10).all()
        if original_dates:
            print("\nRecent dates in News table:")
            # Extract and group by date part
            date_counts = {}
            for date_record in original_dates:
                date_part = date_record[0].split()[0] if ' ' in date_record[0] else date_record[0]
                date_counts[date_part] = date_counts.get(date_part, 0) + 1
            
            for date_str in sorted(date_counts.keys(), reverse=True)[:10]:
                print(f"  {date_str}: {date_counts[date_str]} entries")
                
    except Exception as e:
        print(f"Error listing dates: {e}")
    finally:
        db.close()

def fetch_and_display_analysis(limit=20):
    """
    Fetch the latest news and display their analysis
    """
    print("\n" + "="*60)
    print("FETCHING AND DISPLAYING LATEST NEWS WITH ANALYSIS")
    print("="*60)
    
    # Fetch fresh news from live sources
    print(f"\nFetching {limit} latest news items with dual sentiment analysis...")
    
    # Create database session
    db: Session = SessionLocal()
    
    try:
        # Get the most recent live news with both VADER and FinBERT analysis
        recent_live_news = db.query(LiveNews).order_by(LiveNews.id.desc()).limit(limit).all()
        
        if recent_live_news:
            print(f"\n📊 FOUND {len(recent_live_news)} RECENT NEWS ITEMS WITH DUAL ANALYSIS:")
            print("-" * 80)
            
            # Count sentiment statistics
            vader_pos = vader_neg = vader_neu = 0
            finbert_pos = finbert_neg = finbert_neu = 0
            
            for i, news in enumerate(recent_live_news, 1):
                # Tally sentiment counts
                if news.vader_label.lower() == 'positive':
                    vader_pos += 1
                elif news.vader_label.lower() == 'negative':
                    vader_neg += 1
                else:
                    vader_neu += 1
                    
                if news.finbert_label.lower() == 'positive':
                    finbert_pos += 1
                elif news.finbert_label.lower() == 'negative':
                    finbert_neg += 1
                else:
                    finbert_neu += 1
                
                print(f"\n{i:2d}. 📰 {news.title[:60]}...")
                print(f"     📍 Source: {news.source}")
                print(f"     🕒 Date: {news.date}")
                print(f"     🟢 VADER: {news.vader_label.upper()} (Score: {news.vader_score:.3f})")
                print(f"     🔵 FinBERT: {news.finbert_label.upper()} (Score: {news.finbert_score:.3f})")
                print(f"     🔗 URL: {news.url[:50]}...")
                
            print(f"\n📈 SENTIMENT STATISTICS (Top {limit} news):")
            print(f"   VADER - Positive: {vader_pos}, Negative: {vader_neg}, Neutral: {vader_neu}")
            print(f"   FinBERT - Positive: {finbert_pos}, Negative: {finbert_neg}, Neutral: {finbert_neu}")
        else:
            print("\n❌ No live news found in the database.")
            print("💡 Tip: Run the fetch_and_analyze_latest_news function to populate the database with fresh news.")
            
    except Exception as e:
        print(f"❌ Error fetching recent news: {e}")
    finally:
        db.close()

def fetch_more_live_news(limit=20):
    """
    Helper function to fetch more live news from external sources
    """
    print(f"\n🚀 FETCHING {limit} MORE LIVE NEWS FROM EXTERNAL SOURCES...")
    try:
        from news_fetcher import fetch_and_analyze_latest_news
        result = fetch_and_analyze_latest_news(limit=limit)
        print(f"✅ Successfully fetched and analyzed {result.get('processed', 0)} news items!")
        print("💡 The news has been saved to the database with dual sentiment analysis.")
    except ImportError:
        print("❌ Could not import news_fetcher module")
    except Exception as e:
        print(f"❌ Error fetching live news: {e}")

if __name__ == "__main__":
    print("🔍 Diagnostic script to fetch and analyze news with dual sentiment analysis")
    print("=" * 70)
    
    # First, let's see what dates are available
    list_recent_dates()
    
    # Show most recent news with analysis
    get_most_recent_news(10)
    
    # Fetch and display the latest analysis
    fetch_and_display_analysis(20)
    
    # Option to fetch more news if needed
    print(f"\n💡 If you want to fetch more recent news from live sources,")
    print(f"   you can run the fetch_more_live_news() function separately.")