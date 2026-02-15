'use client';

import { useEffect, useState, useCallback } from 'react';
import { useSearchParams } from 'next/navigation';
import axios from 'axios';
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
  const [error, setError] = useState<string | null>(null);
  const [selectedCoin, setSelectedCoin] = useState<string>(coinFromUrl || 'All');

  const fetchData = useCallback(async (coinQuery: string = '') => {
    try {
      setLoading(true);
      setError(null);

      const statsQuery = coinQuery && coinQuery !== 'All' ? `?q=${encodeURIComponent(coinQuery)}` : '';
      const newsQuery = coinQuery && coinQuery !== 'All' 
        ? `?q=${encodeURIComponent(coinQuery)}&limit=20`
        : '?limit=20';
      
      // Fetch stats and news in parallel
      const [statsResponse, newsResponse] = await Promise.all([
        axios.get<Stats>(`http://127.0.0.1:8000/api/stats${statsQuery}`),
        axios.get<NewsItem[]>(`http://127.0.0.1:8000/api/news${newsQuery}`),
      ]);

      setStats(statsResponse.data);
      setNews(newsResponse.data);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to connect to the API. Make sure the backend server is running on http://127.0.0.1:8000'
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (coinFromUrl) {
      setSelectedCoin(coinFromUrl);
      fetchData(coinFromUrl);
    } else {
      fetchData('');
    }
  }, [coinFromUrl, fetchData]);

  const handleSearch = (query: string) => {
    setSelectedCoin(query || 'All');
    fetchData(query);
  };

  const getDisplayTitle = () => {
    if (selectedCoin && selectedCoin !== 'All') {
      return `${selectedCoin} Sentiment Analysis`;
    }
    return 'Market Sentiment Overview';
  };

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
            </>
          )}
        </div>
      </main>
    </div>
  );
}

