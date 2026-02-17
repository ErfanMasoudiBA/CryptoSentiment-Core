"use client";

import { useState, useEffect } from "react";
import axios from "axios";
import { RefreshCw, ExternalLink, Radio, Calendar } from "lucide-react";
import Sidebar from "../components/Sidebar";
import SentimentChart from "../components/SentimentChart";

interface LiveNewsItem {
  id: number;
  title: string;
  text: string;
  summary: string;
  url: string;
  source: string;
  date: string; // ISO date string
  sentiment: string;
  sentiment_label: string;
  sentiment_score: number;
  vader_label: string;
  vader_score: number;
  finbert_label: string;
  finbert_score: number;
}

export default function LivePage() {
  const [news, setNews] = useState<LiveNewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");
  const [filteredNews, setFilteredNews] = useState<LiveNewsItem[]>([]);

  // Fetch live news on component mount
  useEffect(() => {
    fetchLiveNews();
  }, []);

  // Apply date filters when startDate or endDate changes
  useEffect(() => {
    if (news.length > 0) {
      let filtered = [...news];

      if (startDate) {
        filtered = filtered.filter(
          (item) => new Date(item.date) >= new Date(startDate)
        );
      }

      if (endDate) {
        filtered = filtered.filter(
          (item) => new Date(item.date) <= new Date(endDate)
        );
      }

      setFilteredNews(filtered);
    }
  }, [startDate, endDate, news]);

  const fetchLiveNews = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get<LiveNewsItem[]>(
        "http://127.0.0.1:8000/api/live_news"
      );
      setNews(response.data);
      setFilteredNews(response.data); // Initially show all news
    } catch (err) {
      console.error("Error fetching live news:", err);
      setError(
        err instanceof Error
          ? err.message
          : "Failed to connect to the API. Make sure the backend server is running on http://127.0.0.1:8000"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleSyncNews = async () => {
    try {
      setSyncing(true);
      setError(null);

      // Trigger the sync endpoint with a limit of 5
      await axios.post("http://127.0.0.1:8000/api/fetch_live_news", null, {
        params: { limit: 5 },
      });

      // Refresh the news after sync completes
      await fetchLiveNews();
    } catch (err) {
      console.error("Error syncing live news:", err);
      setError(
        err instanceof Error
          ? err.message
          : "Failed to sync live news. Make sure the backend server is running on http://127.0.0.1:8000"
      );
    } finally {
      setSyncing(false);
    }
  };

  const handleDateFilter = () => {
    // The filtering is handled by the useEffect
  };

  // Format date to a readable format
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  // Get sentiment badge color based on label
  const getSentimentColor = (label: string) => {
    switch (label.toLowerCase()) {
      case "positive":
        return "bg-green-500/20 text-green-400 border-green-500/30";
      case "negative":
        return "bg-red-500/20 text-red-400 border-red-500/30";
      default:
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30";
    }
  };

  // Calculate market sentiment statistics for filtered news
  const calculateSentimentStats = () => {
    const total = filteredNews.length;
    if (total === 0)
      return { positive: 0, negative: 0, neutral: 0, avgScore: 0 };

    const positive = filteredNews.filter(
      (item) => item.sentiment_label.toLowerCase() === "positive"
    ).length;
    const negative = filteredNews.filter(
      (item) => item.sentiment_label.toLowerCase() === "negative"
    ).length;
    const neutral = total - positive - negative;

    const avgScore =
      filteredNews.reduce((sum, item) => sum + item.sentiment_score, 0) / total;

    return { positive, negative, neutral, avgScore };
  };

  // Calculate market sentiment statistics for FinBERT for filtered news
  const calculateFinbertStats = () => {
    const total = filteredNews.length;
    if (total === 0)
      return { positive: 0, negative: 0, neutral: 0, avgScore: 0 };

    const positive = filteredNews.filter(
      (item) => item.finbert_label.toLowerCase() === "positive"
    ).length;
    const negative = filteredNews.filter(
      (item) => item.finbert_label.toLowerCase() === "negative"
    ).length;
    const neutral = total - positive - negative;

    const avgScore =
      filteredNews.reduce((sum, item) => sum + item.finbert_score, 0) / total;

    return { positive, negative, neutral, avgScore };
  };

  // Calculate market sentiment statistics for VADER for filtered news
  const calculateVaderStats = () => {
    const total = filteredNews.length;
    if (total === 0)
      return { positive: 0, negative: 0, neutral: 0, avgScore: 0 };

    const positive = filteredNews.filter(
      (item) => item.vader_label.toLowerCase() === "positive"
    ).length;
    const negative = filteredNews.filter(
      (item) => item.vader_label.toLowerCase() === "negative"
    ).length;
    const neutral = total - positive - negative;

    const avgScore =
      filteredNews.reduce((sum, item) => sum + item.vader_score, 0) / total;

    return { positive, negative, neutral, avgScore };
  };

  const {
    positive: finbertPositive,
    negative: finbertNegative,
    neutral: finbertNeutral,
    avgScore: finbertAvgScore,
  } = calculateFinbertStats();
  const {
    positive: vaderPositive,
    negative: vaderNegative,
    neutral: vaderNeutral,
    avgScore: vaderAvgScore,
  } = calculateVaderStats();

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <Sidebar />

      <main className="flex-1 p-8">
        <div className="max-w-7xl mx-auto space-y-6">
          {/* Header with date filters */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="relative">
                <Radio className="text-red-500 animate-pulse" size={28} />
                <div className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full animate-ping"></div>
              </div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-red-400 to-orange-400 bg-clip-text text-transparent">
                Live Market Pulse
              </h1>
            </div>

            <div className="flex items-center gap-4">
              {/* Date Range Filter */}
              <div className="flex items-center gap-2">
                <Calendar size={20} className="text-blue-400" />
                <div className="flex gap-2">
                  <div>
                    <label htmlFor="start-date" className="sr-only">
                      Start Date
                    </label>
                    <input
                      id="start-date"
                      type="date"
                      value={startDate}
                      onChange={(e) => setStartDate(e.target.value)}
                      className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <span className="text-slate-400 self-center">to</span>
                  <div>
                    <label htmlFor="end-date" className="sr-only">
                      End Date
                    </label>
                    <input
                      id="end-date"
                      type="date"
                      value={endDate}
                      onChange={(e) => setEndDate(e.target.value)}
                      className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>
                <button
                  onClick={handleDateFilter}
                  className="px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                >
                  Filter
                </button>
              </div>

              <button
                onClick={handleSyncNews}
                disabled={syncing}
                className="px-6 py-3 bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 disabled:from-slate-600 disabled:to-slate-600 text-white font-medium rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl flex items-center gap-2"
              >
                {syncing ? (
                  <>
                    <RefreshCw className="animate-spin" size={20} />
                    Syncing...
                  </>
                ) : (
                  <>
                    <RefreshCw size={20} />
                    Sync Latest News
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Market Sentiment Analysis */}
          {!loading && (
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 shadow-lg p-6">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <Radio size={20} className="text-red-500" />
                Live Market Sentiment Analysis
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="flex flex-col items-center justify-center">
                  <div className="w-full max-w-md flex justify-center">
                    <SentimentChart
                      positive={finbertPositive}
                      negative={finbertNegative}
                      neutral={finbertNeutral}
                      coinName="FinBERT"
                    />
                  </div>
                </div>
                <div className="flex flex-col items-center justify-center">
                  <div className="w-full max-w-md flex justify-center">
                    <SentimentChart
                      positive={vaderPositive}
                      negative={vaderNegative}
                      neutral={vaderNeutral}
                      coinName="VADER"
                    />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="bg-red-500/10 border border-red-500/50 rounded-xl p-6 shadow-lg">
              <h3 className="text-red-400 font-semibold mb-2">Error</h3>
              <p className="text-red-300">{error}</p>
              <p className="text-red-300/70 text-sm mt-2">
                Please ensure the FastAPI backend is running on
                http://127.0.0.1:8000
              </p>
            </div>
          )}

          {/* Loading State */}
          {loading && !syncing && (
            <div className="flex items-center justify-center py-20">
              <div className="text-center">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-slate-600 border-t-red-500 mb-4"></div>
                <p className="text-slate-400">Loading live market data...</p>
              </div>
            </div>
          )}

          {/* News Grid */}
          {!loading && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredNews.length === 0 ? (
                <div className="col-span-full text-center py-12">
                  <div className="mx-auto w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center mb-4">
                    <Radio className="text-slate-600" size={32} />
                  </div>
                  <h3 className="text-xl font-semibold text-slate-400 mb-2">
                    {news.length === 0
                      ? "No live news yet"
                      : "No news in selected date range"}
                  </h3>
                  <p className="text-slate-500 mb-4">
                    {news.length === 0
                      ? 'Click "Sync Latest News" to fetch the latest cryptocurrency news'
                      : "Try adjusting the date range to see more news"}
                  </p>
                  <button
                    onClick={handleSyncNews}
                    disabled={syncing}
                    className="px-4 py-2 bg-slate-700 hover:bg-slate-600 disabled:opacity-50 text-white rounded-lg transition-colors flex items-center gap-2 mx-auto"
                  >
                    {syncing ? (
                      <>
                        <RefreshCw className="animate-spin" size={16} />
                        Syncing...
                      </>
                    ) : (
                      <>
                        <RefreshCw size={16} />
                        Fetch News
                      </>
                    )}
                  </button>
                </div>
              ) : (
                filteredNews.map((item) => (
                  <div
                    key={item.id}
                    className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 shadow-lg overflow-hidden hover:border-slate-600/50 transition-all duration-200 hover:shadow-xl"
                  >
                    <div className="p-6">
                      <div className="flex justify-between items-start mb-3">
                        <span className="text-xs font-medium text-slate-400 bg-slate-700/50 px-2 py-1 rounded">
                          {item.source}
                        </span>
                        <span className="text-xs text-slate-500">
                          {formatDate(item.date)}
                        </span>
                      </div>

                      <h3 className="font-semibold text-white mb-3 line-clamp-3 leading-tight">
                        {item.title}
                      </h3>

                      <div className="flex items-center justify-between">
                        <div className="flex flex-col gap-1">
                          <div className="flex gap-2">
                            <span
                              className={`text-xs font-medium px-2 py-1 rounded-full border ${getSentimentColor(
                                item.finbert_label
                              )}`}
                            >
                              F:{" "}
                              {item.finbert_label.charAt(0).toUpperCase() +
                                item.finbert_label.slice(1)}
                            </span>
                            <span
                              className={`text-xs font-medium px-2 py-1 rounded-full border ${getSentimentColor(
                                item.vader_label
                              )}`}
                            >
                              V:{" "}
                              {item.vader_label.charAt(0).toUpperCase() +
                                item.vader_label.slice(1)}
                            </span>
                          </div>
                          <div className="flex gap-2 text-xs text-slate-400">
                            <span>
                              F: {(item.finbert_score * 100).toFixed(1)}%
                            </span>
                            <span>
                              V: {(item.vader_score * 100).toFixed(1)}%
                            </span>
                          </div>
                        </div>

                        <a
                          href={item.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs bg-slate-700 hover:bg-slate-600 text-slate-200 px-3 py-1.5 rounded-lg transition-colors flex items-center gap-1"
                        >
                          Read Original
                          <ExternalLink size={12} />
                        </a>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {/* Footer */}
          <footer className="pt-8 pb-4 text-center text-slate-500 text-sm">
            Real-time cryptocurrency news monitoring • Updated as new events
            occur
          </footer>
        </div>
      </main>
    </div>
  );
}
