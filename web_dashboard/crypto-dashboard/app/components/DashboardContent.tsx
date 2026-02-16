'use client';

import { useEffect, useState, useCallback } from 'react';
import { useSearchParams } from 'next/navigation';
import axios from 'axios';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import Sidebar from './Sidebar';
import SentimentChart from './SentimentChart';
import NewsTable from './NewsTable';
import SearchBar from './SearchBar';

interface Stats {
  total: number;
  positive: number;
  negative: number;
  neutral: number;
}

interface NewsItem {
  id: number;
  title: string;
  summary: string;
  source: string;
  url: string;
  published_date: string;
  sentiment_label: string;
  sentiment_score: number;
}

const PAGE_SIZE = 20;

export default function DashboardContent() {
  const searchParams = useSearchParams();
  const coinFromUrl = searchParams.get('coin') || '';

  const [stats, setStats] = useState<Stats>({
    total: 0,
    positive: 0,
    negative: 0,
    neutral: 0,
  });
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedCoin, setSelectedCoin] = useState<string>(coinFromUrl || 'All');
  const [currentPage, setCurrentPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);

  const fetchData = useCallback(async (coinQuery: string = '', page: number = 0, append: boolean = false) => {
    try {
      if (append) {
        setLoadingMore(true);
      } else {
        setLoading(true);
      }
      setError(null);

      const statsQuery = coinQuery && coinQuery !== 'All' ? `?q=${encodeURIComponent(coinQuery)}` : '';
      const skip = page * PAGE_SIZE;
      const newsQuery = coinQuery && coinQuery !== 'All' 
        ? `?q=${encodeURIComponent(coinQuery)}&skip=${skip}&limit=${PAGE_SIZE}`
        : `?skip=${skip}&limit=${PAGE_SIZE}`;
      
      // Fetch stats and news in parallel
      const [statsResponse, newsResponse] = await Promise.all([
        axios.get<Stats>(`http://127.0.0.1:8000/api/stats${statsQuery}`),
        axios.get<NewsItem[]>(`http://127.0.0.1:8000/api/news${newsQuery}`),
      ]);

      setStats(statsResponse.data);
      
      if (append) {
        setNews(prev => [...prev, ...newsResponse.data]);
      } else {
        setNews(newsResponse.data);
      }
      
      // Check if there are more items
      setHasMore(newsResponse.data.length === PAGE_SIZE);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to connect to the API. Make sure the backend server is running on http://127.0.0.1:8000'
      );
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  }, []);

  useEffect(() => {
    if (coinFromUrl) {
      setSelectedCoin(coinFromUrl);
      setCurrentPage(0);
      fetchData(coinFromUrl, 0, false);
    } else {
      setCurrentPage(0);
      fetchData('', 0, false);
    }
  }, [coinFromUrl, fetchData]);

  const handleSearch = (query: string) => {
    setSelectedCoin(query || 'All');
    setCurrentPage(0);
    fetchData(query, 0, false);
  };

  const handleLoadMore = () => {
    const nextPage = currentPage + 1;
    setCurrentPage(nextPage);
    fetchData(selectedCoin === 'All' ? '' : selectedCoin, nextPage, true);
  };

  const handlePageChange = (newPage: number) => {
    setCurrentPage(newPage);
    fetchData(selectedCoin === 'All' ? '' : selectedCoin, newPage, false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const getDisplayTitle = () => {
    if (selectedCoin && selectedCoin !== 'All') {
      return `${selectedCoin} Sentiment Analysis`;
    }
    return 'Market Sentiment Overview';
  };

  const totalPages = Math.ceil(news.length / PAGE_SIZE) + (hasMore ? 1 : 0);

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <Sidebar />
      
      <main className="flex-1 p-8">
        <div className="max-w-7xl mx-auto space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Dashboard
              </h1>
              <p className="text-slate-400">{getDisplayTitle()}</p>
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50 shadow-lg relative z-50">
            <SearchBar onSearch={handleSearch} selectedCoin={selectedCoin} />
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-20">
              <div className="text-center">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-slate-600 border-t-blue-500 mb-4"></div>
                <p className="text-slate-400">Loading data...</p>
              </div>
            </div>
          ) : error ? (
            <div className="bg-red-500/10 border border-red-500/50 rounded-xl p-6 shadow-lg">
              <h3 className="text-red-400 font-semibold mb-2">Error</h3>
              <p className="text-red-300">{error}</p>
              <p className="text-red-300/70 text-sm mt-2">
                Please ensure the FastAPI backend is running on http://127.0.0.1:8000
              </p>
            </div>
          ) : (
            <>
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 shadow-lg p-6">
                <SentimentChart
                  positive={stats.positive}
                  negative={stats.negative}
                  neutral={stats.neutral}
                  coinName={selectedCoin && selectedCoin !== 'All' ? selectedCoin : undefined}
                />
              </div>
              
              <NewsTable news={news} />
              
              {/* Pagination Controls */}
              <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div className="text-slate-400 text-sm">
                    Showing {news.length} {news.length === 1 ? 'article' : 'articles'}
                    {selectedCoin !== 'All' && ` for ${selectedCoin}`}
                  </div>
                  
                  <div className="flex items-center gap-2">
                    {hasMore && (
                      <button
                        onClick={handleLoadMore}
                        disabled={loadingMore}
                        className="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:opacity-50 text-white font-medium rounded-lg transition-colors shadow-md hover:shadow-lg flex items-center gap-2"
                      >
                        {loadingMore ? (
                          <>
                            <div className="inline-block animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                            <span>Loading...</span>
                          </>
                        ) : (
                          <>
                            <span>Load More</span>
                            <ChevronRight size={18} />
                          </>
                        )}
                      </button>
                    )}
                    
                    {!hasMore && news.length > 0 && (
                      <span className="text-slate-400 text-sm">No more articles to load</span>
                    )}
                  </div>
                </div>
              </div>

              {/* Footer */}
              <footer className="pt-8 pb-4 text-center text-slate-500 text-sm">
                Powered by FinBERT & VADER | © 2024 CryptoSentiment Project
              </footer>
            </>
          )}
        </div>
      </main>
    </div>
  );
}
