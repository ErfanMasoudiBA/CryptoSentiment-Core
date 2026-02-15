'use client';

import { ExternalLink, TrendingUp, TrendingDown, Minus } from 'lucide-react';

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

interface NewsListProps {
  news: NewsItem[];
}

export default function NewsList({ news }: NewsListProps) {
  const getSentimentIcon = (label: string) => {
    switch (label.toLowerCase()) {
      case 'positive':
        return <TrendingUp className="text-green-400" size={20} />;
      case 'negative':
        return <TrendingDown className="text-red-400" size={20} />;
      default:
        return <Minus className="text-slate-400" size={20} />;
    }
  };

  const getSentimentColor = (label: string) => {
    switch (label.toLowerCase()) {
      case 'positive':
        return 'border-l-green-500 bg-green-500/10';
      case 'negative':
        return 'border-l-red-500 bg-red-500/10';
      default:
        return 'border-l-slate-500 bg-slate-500/10';
    }
  };

  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    } catch {
      return dateString;
    }
  };

  if (news.length === 0) {
    return (
      <div className="bg-slate-800 rounded-lg p-8 border border-slate-700">
        <p className="text-slate-400 text-center">No news available</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700">
      <div className="p-6 border-b border-slate-700">
        <h2 className="text-xl font-bold text-white">Latest News</h2>
      </div>
      
      <div className="divide-y divide-slate-700">
        {news.map((item) => (
          <div
            key={item.id}
            className={`p-6 border-l-4 hover:bg-slate-700/50 transition-colors ${getSentimentColor(
              item.sentiment_label
            )}`}
          >
            <div className="flex items-start gap-4">
              <div className="mt-1">{getSentimentIcon(item.sentiment_label)}</div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-4 mb-2">
                  <h3 className="text-lg font-semibold text-white hover:text-blue-400 transition-colors">
                    {item.title}
                  </h3>
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300 flex-shrink-0"
                    title="Open article"
                  >
                    <ExternalLink size={18} />
                  </a>
                </div>
                
                <p className="text-slate-300 text-sm mb-3 line-clamp-2">
                  {item.summary}
                </p>
                
                <div className="flex items-center justify-between text-xs text-slate-400">
                  <div className="flex items-center gap-4">
                    <span className="font-medium">{item.source}</span>
                    <span>•</span>
                    <span>{formatDate(item.published_date)}</span>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <span
                      className={`px-2 py-1 rounded ${
                        item.sentiment_label.toLowerCase() === 'positive'
                          ? 'bg-green-500/20 text-green-400'
                          : item.sentiment_label.toLowerCase() === 'negative'
                          ? 'bg-red-500/20 text-red-400'
                          : 'bg-slate-500/20 text-slate-400'
                      }`}
                    >
                      {item.sentiment_label}
                    </span>
                    <span className="text-slate-500">
                      Score: {(item.sentiment_score * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

