#!/usr/bin/env python3
"""
Diagnostic script to verify the Live News feature in the backend system.
This script checks if all components of the live news functionality work correctly.
"""

import traceback
from sqlalchemy import inspect
from database import engine, Base, LiveNews
from news_fetcher import fetch_and_analyze_latest_news
from sqlalchemy.orm import Session
from database import SessionLocal


def check_database_table():
    """Check if the live_news table exists in the database."""
    print("🔍 Checking database table...")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if 'live_news' in tables:
        print("✅ Table 'live_news' exists in the database")
        return True
    else:
        print("❌ Table 'live_news' does not exist in the database")
        print("🔧 Attempting to create the table...")
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Table 'live_news' created successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to create table: {str(e)}")
            return False


def test_fetch_function():
    """Test the fetch_and_analyze_latest_news function directly."""
    print("\n🔍 Testing fetch_and_analyze_latest_news function...")
    try:
        result = fetch_and_analyze_latest_news(limit=2)
        print(f"✅ Fetch function executed successfully: {result}")
        return result
    except Exception as e:
        print(f"❌ Error in fetch function: {str(e)}")
        traceback.print_exc()
        return None


def verify_saved_data():
    """Query the LiveNews table to verify new entries were added."""
    print("\n🔍 Verifying saved news in database...")
    try:
        db: Session = SessionLocal()
        
        # Count records before
        initial_count = db.query(LiveNews).count()
        print(f"📊 Initial record count: {initial_count}")
        
        # Fetch and analyze 2 news items
        print("🔄 Calling fetch_and_analyze_latest_news with limit=2...")
        result = fetch_and_analyze_latest_news(limit=2)
        print(f"📋 Fetch result: {result}")
        
        # Count records after
        final_count = db.query(LiveNews).count()
        print(f"📊 Final record count: {final_count}")
        
        added_count = final_count - initial_count
        print(f"📈 Records added: {added_count}")
        
        # Query the latest records to show their content
        latest_news = db.query(LiveNews).order_by(LiveNews.id.desc()).limit(5).all()
        
        if latest_news:
            print("\n📰 Latest saved news:")
            print("-" * 80)
            for i, news in enumerate(latest_news[:2]):  # Show first 2
                print(f"Title: {news.title[:100]}{'...' if len(news.title) > 100 else ''}")
                print(f"Sentiment Label: {news.sentiment_label}")
                print(f"Sentiment Score: {news.sentiment_score}")
                print("-" * 80)
        else:
            print("❌ No news records found in the database")
        
        db.close()
        return {
            "initial_count": initial_count,
            "final_count": final_count,
            "added_count": added_count,
            "latest_news": latest_news
        }
        
    except Exception as e:
        print(f"❌ Error querying database: {str(e)}")
        traceback.print_exc()
        return None


def main():
    """Main diagnostic function."""
    print("=" * 60)
    print("🔧 DIAGNOSTIC SCRIPT FOR LIVE NEWS FEATURE")
    print("=" * 60)
    
    # Step 1: Check if database table exists
    table_ok = check_database_table()
    
    if not table_ok:
        print("\n❌ Database table check failed. Cannot proceed with other tests.")
        return
    
    # Step 2: Test the fetch function
    fetch_result = test_fetch_function()
    
    if fetch_result is None:
        print("\n❌ Fetch function test failed.")
        return
    
    # Step 3: Verify that data was saved properly
    verification_result = verify_saved_data()
    
    if verification_result is None:
        print("\n❌ Data verification failed.")
        return
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    initial_count = verification_result["initial_count"]
    final_count = verification_result["final_count"]
    added_count = verification_result["added_count"]
    
    print(f"✅ Database table: 'live_news' exists and is accessible")
    print(f"✅ Fetch function: executed successfully")
    print(f"📊 Records before test: {initial_count}")
    print(f"📊 Records after test: {final_count}")
    print(f"📈 New records added: {added_count}")
    
    if added_count > 0:
        print("🎉 SUCCESS: Live News feature is working correctly!")
        print("✅ News items are being fetched, analyzed, and saved to the database")
    else:
        print("⚠️  WARNING: No new records were added. This might be because:")
        print("   - All fetched news items already exist in the database (duplicate check)")
        print("   - The API returned no new articles")
        print("   - There might be an issue with the duplicate detection logic")
    
    print("\n🎯 The diagnostic is complete!")


if __name__ == "__main__":
    main()