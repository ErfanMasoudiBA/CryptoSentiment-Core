#!/usr/bin/env python3
"""
Test script to verify the enhanced news fetcher functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from news_fetcher import fetch_and_analyze_latest_news

def test_enhanced_fetcher():
    print("🧪 Testing Enhanced News Fetcher...")
    print("This test will fetch news from multiple sources including RSS feeds...")
    
    try:
        result = fetch_and_analyze_latest_news(limit=3)
        print(f"✅ Fetch completed: {result}")
        
        # Also test individual sources
        from news_fetcher import fetch_cryptocompare_news, fetch_cointelegraph_news, fetch_coindesk_news
        
        print("\n🔍 Testing individual sources:")
        
        cc_result = fetch_cryptocompare_news(2)
        print(f"CryptoCompare: {len(cc_result)} articles")
        
        ct_result = fetch_cointelegraph_news(2)
        print(f"CoinTelegraph: {len(ct_result)} articles")
        
        cd_result = fetch_coindesk_news(2)
        print(f"CoinDesk: {len(cd_result)} articles")
        
        print("\n🎉 All tests completed successfully!")
        print("The enhanced news fetcher is working with multiple sources.")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_enhanced_fetcher()