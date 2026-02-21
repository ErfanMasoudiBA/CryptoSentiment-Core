"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import Sidebar from "../components/Sidebar";
import { TrendingUp, TrendingDown, Minus, ArrowRight } from "lucide-react";

interface CoinData {
  name: string;
  symbol: string;
  stats: {
    total: number;
    positive: number;
    negative: number;
    neutral: number;
  };
}

const coins = [
  { name: "Bitcoin", symbol: "BTC" },
  { name: "Ethereum", symbol: "ETH" },
  { name: "Ripple", symbol: "XRP" },
  { name: "Litecoin", symbol: "LTC" },
  { name: "Dogecoin", symbol: "DOGE" },
  { name: "Cardano", symbol: "ADA" },
  { name: "Solana", symbol: "SOL" },
  { name: "Polkadot", symbol: "DOT" },
  { name: "Chainlink", symbol: "LINK" },
  { name: "Binance Coin", symbol: "BNB" },
];

export default function MarketPage() {
  const router = useRouter();
  const [coinsData, setCoinsData] = useState<CoinData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCoinsData = async () => {
      try {
        setLoading(true);
        setError(null);

        const promises = coins.map(async (coin) => {
          try {
            const response = await axios.get(
              `http://127.0.0.1:8000/api/stats?q=${encodeURIComponent(
                coin.name
              )}`
            );
            return {
              name: coin.name,
              symbol: coin.symbol,
              stats: response.data,
            };
          } catch (err) {
            return {
              name: coin.name,
              symbol: coin.symbol,
              stats: { total: 0, positive: 0, negative: 0, neutral: 0 },
            };
          }
        });

        const results = await Promise.all(promises);
        setCoinsData(results);
      } catch (err) {
        console.error("Error fetching coins data:", err);
        setError("Failed to load market data");
      } finally {
        setLoading(false);
      }
    };

    fetchCoinsData();
  }, []);

  const getOverallSentiment = (stats: CoinData["stats"]) => {
    if (stats.total === 0) return { label: "No Data", color: "text-slate-400" };

    const positiveRatio = stats.positive / stats.total;
    const negativeRatio = stats.negative / stats.total;

    if (positiveRatio > negativeRatio && positiveRatio > 0.4) {
      return { label: "Positive", color: "text-green-400" };
    } else if (negativeRatio > positiveRatio && negativeRatio > 0.4) {
      return { label: "Negative", color: "text-red-400" };
    } else {
      return { label: "Neutral", color: "text-slate-400" };
    }
  };

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case "Positive":
        return <TrendingUp className="text-green-400" size={20} />;
      case "Negative":
        return <TrendingDown className="text-red-400" size={20} />;
      default:
        return <Minus className="text-slate-400" size={20} />;
    }
  };

  const handleViewDetails = (coinName: string) => {
    router.push(`/?coin=${encodeURIComponent(coinName)}`);
  };

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <Sidebar />

      <main className="flex-1 p-4 md:p-6 lg:p-8">
        <div className="max-w-7xl mx-auto space-y-6">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              Market Overview
            </h1>
            <p className="text-slate-400">
              Explore sentiment analysis for different cryptocurrencies
            </p>
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-16 md:py-20">
              <div className="text-center max-w-sm w-full">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-slate-600 border-t-blue-500 mb-4"></div>
                <p className="text-slate-400">Loading market data...</p>
              </div>
            </div>
          ) : error ? (
            <div className="bg-red-500/10 border border-red-500/50 rounded-xl p-4 md:p-6 shadow-lg">
              <h3 className="text-red-400 font-semibold mb-2">Error</h3>
              <p className="text-red-300">{error}</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
              {coinsData.map((coin) => {
                const sentiment = getOverallSentiment(coin.stats);
                return (
                  <div
                    key={coin.name}
                    className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 shadow-lg hover:shadow-xl transition-all-fast hover:border-blue-500/50 p-4 md:p-6"
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h3 className="text-lg md:text-xl font-bold text-white mb-1">
                          {coin.name}
                        </h3>
                        <p className="text-sm text-slate-400">{coin.symbol}</p>
                      </div>
                      <div className="bg-blue-600/20 rounded-lg p-2">
                        {getSentimentIcon(sentiment.label)}
                      </div>
                    </div>

                    <div className="mb-4">
                      <p className="text-xs text-slate-400 mb-1">
                        Overall Sentiment
                      </p>
                      <p className={`text-lg font-semibold ${sentiment.color}`}>
                        {sentiment.label}
                      </p>
                    </div>

                    <div className="grid grid-cols-3 gap-2 mb-4 text-xs">
                      <div className="text-center p-2 bg-green-500/10 rounded-lg border border-green-500/20">
                        <div className="text-green-400 font-bold">
                          {coin.stats.positive}
                        </div>
                        <div className="text-slate-400">Positive</div>
                      </div>
                      <div className="text-center p-2 bg-red-500/10 rounded-lg border border-red-500/20">
                        <div className="text-red-400 font-bold">
                          {coin.stats.negative}
                        </div>
                        <div className="text-slate-400">Negative</div>
                      </div>
                      <div className="text-center p-2 bg-slate-500/10 rounded-lg border border-slate-500/20">
                        <div className="text-slate-400 font-bold">
                          {coin.stats.neutral}
                        </div>
                        <div className="text-slate-400">Neutral</div>
                      </div>
                    </div>

                    <button
                      onClick={() => handleViewDetails(coin.name)}
                      className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-all-fast shadow-md hover:shadow-lg touch-target"
                    >
                      <span>View Details</span>
                      <ArrowRight size={16} />
                    </button>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
