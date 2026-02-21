"use client";

import { ExternalLink, TrendingUp, TrendingDown, Minus } from "lucide-react";

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

interface NewsTableProps {
  news: NewsItem[];
}

export default function NewsTable({ news }: NewsTableProps) {
  const getSentimentIcon = (label: string) => {
    switch (label.toLowerCase()) {
      case "positive":
        return <TrendingUp className="text-green-400" size={18} />;
      case "negative":
        return <TrendingDown className="text-red-400" size={18} />;
      default:
        return <Minus className="text-slate-400" size={18} />;
    }
  };

  const getSentimentBadge = (label: string) => {
    switch (label.toLowerCase()) {
      case "positive":
        return "bg-green-500/20 text-green-400 border-green-500/30";
      case "negative":
        return "bg-red-500/20 text-red-400 border-red-500/30";
      default:
        return "bg-slate-500/20 text-slate-400 border-slate-500/30";
    }
  };

  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    } catch {
      return dateString;
    }
  };

  if (news.length === 0) {
    return (
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-8 border border-slate-700/50 shadow-lg">
        <p className="text-slate-400 text-center">No news available</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 shadow-lg overflow-hidden fade-in">
      <div className="p-4 md:p-6 border-b border-slate-700/50 bg-slate-800/30">
        <h2 className="text-lg md:text-xl font-bold text-white">Latest News</h2>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[800px] md:min-w-0">
          <thead className="bg-slate-800/30 border-b border-slate-700/50">
            <tr>
              <th className="px-4 py-3 md:px-6 md:py-4 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Sentiment
              </th>
              <th className="px-4 py-3 md:px-6 md:py-4 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Title
              </th>
              <th className="px-4 py-3 md:px-6 md:py-4 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider hidden sm:table-cell">
                Source
              </th>
              <th className="px-4 py-3 md:px-6 md:py-4 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider hidden md:table-cell">
                Date
              </th>
              <th className="px-4 py-3 md:px-6 md:py-4 text-left text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Score
              </th>
              <th className="px-4 py-3 md:px-6 md:py-4 text-center text-xs font-semibold text-slate-400 uppercase tracking-wider">
                Action
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/30">
            {news.map((item) => (
              <tr
                key={item.id}
                className="hover:bg-slate-700/20 transition-all-fast"
              >
                <td className="px-4 py-3 md:px-6 md:py-4 whitespace-nowrap">
                  <div className="flex items-center gap-2">
                    {getSentimentIcon(item.sentiment_label)}
                    <span
                      className={`px-2 py-1 rounded-md text-xs font-medium border ${getSentimentBadge(
                        item.sentiment_label
                      )}`}
                    >
                      {item.sentiment_label}
                    </span>
                  </div>
                </td>
                <td className="px-4 py-3 md:px-6 md:py-4">
                  <div className="max-w-xs md:max-w-md">
                    <div className="text-sm font-semibold text-white mb-1 line-clamp-2 md:line-clamp-1">
                      {item.title}
                    </div>
                    <div className="text-xs text-slate-400 line-clamp-2 hidden md:block">
                      {item.summary}
                    </div>
                  </div>
                </td>
                <td className="px-4 py-3 md:px-6 md:py-4 whitespace-nowrap hidden sm:table-cell">
                  <span className="text-sm text-slate-300">{item.source}</span>
                </td>
                <td className="px-4 py-3 md:px-6 md:py-4 whitespace-nowrap hidden md:table-cell">
                  <span className="text-sm text-slate-400">
                    {formatDate(item.published_date)}
                  </span>
                </td>
                <td className="px-4 py-3 md:px-6 md:py-4 whitespace-nowrap">
                  <span className="text-sm font-medium text-slate-300">
                    {(item.sentiment_score * 100).toFixed(1)}%
                  </span>
                </td>
                <td className="px-4 py-3 md:px-6 md:py-4 whitespace-nowrap text-center">
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 md:gap-2 px-3 py-2 md:px-4 md:py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs md:text-sm font-semibold rounded-lg transition-colors shadow-md hover:shadow-lg border-0 touch-target"
                  >
                    <span className="hidden xs:inline">Read More</span>
                    <ExternalLink size={14} />
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
