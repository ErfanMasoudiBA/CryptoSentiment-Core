"use client";

import { useState } from "react";
import axios from "axios";
import Sidebar from "../components/Sidebar";
import { Sparkles, Loader2 } from "lucide-react";

const API_BASE = "http://127.0.0.1:8000";

interface AnalyzeResult {
  label: string;
  score: number;
  error?: string;
}

const SAMPLE_SCENARIOS = [
  {
    label: "Supply Shock",
    text: "The sudden supply shock caused the price to stabilize at a higher level.",
  },
  {
    label: "Regulations",
    text: "The strict regulations were finally lifted, opening doors for massive adoption.",
  },
  {
    label: "Insured Hack",
    text: "The hack resulted in zero loss of user funds due to insurance coverage.",
  },
];

export default function PlaygroundPage() {
  const [text, setText] = useState("");
  const [model, setModel] = useState<"vader" | "finbert">("vader");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    setError(null);
    setResult(null);
    if (!text.trim()) {
      setError("Please enter some text to analyze.");
      return;
    }
    setLoading(true);
    try {
      const { data } = await axios.post<AnalyzeResult>(
        `${API_BASE}/api/analyze_text`,
        {
          text: text.trim(),
          model,
        }
      );
      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to analyze. Is the backend running on http://127.0.0.1:8000?"
      );
    } finally {
      setLoading(false);
    }
  };

  const fillSample = (sampleText: string) => {
    setText(sampleText);
    setError(null);
    setResult(null);
  };

  const getResultStyles = () => {
    if (!result) return {};
    const label = result.label?.toLowerCase() ?? "neutral";
    if (label === "positive")
      return {
        bg: "bg-green-500/20 border-green-500/50",
        text: "text-green-400",
        label: "Positive",
      };
    if (label === "negative")
      return {
        bg: "bg-red-500/20 border-red-500/50",
        text: "text-red-400",
        label: "Negative",
      };
    return {
      bg: "bg-slate-500/20 border-slate-500/50",
      text: "text-slate-400",
      label: "Neutral",
    };
  };

  const formatScore = (score: number) => {
    const pct = model === "vader" ? ((score + 1) / 2) * 100 : score * 100;
    return `${Math.round(Math.max(0, Math.min(100, pct)))}%`;
  };

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <Sidebar />
      <main className="flex-1 p-4 md:p-6 lg:p-8">
        <div className="max-w-3xl mx-auto space-y-6 md:space-y-8">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              AI Sentiment Lab
            </h1>
            <p className="text-slate-400">Compare VADER vs FinBERT models</p>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 shadow-lg p-4 md:p-6 space-y-4">
            <label className="block text-sm font-medium text-slate-300">
              Input text
            </label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Type a news headline here..."
              rows={5}
              className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-y touch-target"
            />

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Model
              </label>
              <select
                value={model}
                onChange={(e) =>
                  setModel(e.target.value as "vader" | "finbert")
                }
                className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent touch-target"
              >
                <option value="vader">VADER (Lexicon Based)</option>
                <option value="finbert">FinBERT (Transformer Based)</option>
              </select>
            </div>

            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 px-4 py-3 md:px-6 md:py-4 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-800 disabled:opacity-70 text-white font-semibold rounded-xl transition-all-fast shadow-lg hover:shadow-xl touch-target"
            >
              {loading ? (
                <>
                  <Loader2 size={20} className="animate-spin" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <Sparkles size={20} />
                  <span>Analyze Sentiment</span>
                </>
              )}
            </button>
          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-500/50 rounded-xl p-4">
              <p className="text-red-400">{error}</p>
            </div>
          )}

          {result && (
            <div
              className={`rounded-xl border p-4 md:p-6 ${getResultStyles().bg}`}
            >
              <p className="text-sm font-medium text-slate-400 mb-1">
                Sentiment
              </p>
              <p
                className={`text-2xl md:text-3xl font-bold ${
                  getResultStyles().text
                }`}
              >
                {getResultStyles().label}
              </p>
              <p className="text-slate-300 mt-2">
                Confidence:{" "}
                <span className="font-semibold text-white">
                  {formatScore(result.score)}
                </span>
              </p>
              {result.error && (
                <p className="text-amber-400 text-sm mt-2">{result.error}</p>
              )}
            </div>
          )}

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 shadow-lg p-4 md:p-6">
            <h3 className="text-lg font-semibold text-white mb-3">
              Sample Scenarios
            </h3>
            <p className="text-slate-400 text-sm mb-4">
              Click to fill the textarea with sample text.
            </p>
            <div className="flex flex-wrap gap-2 md:gap-3">
              {SAMPLE_SCENARIOS.map((sample) => (
                <button
                  key={sample.label}
                  onClick={() => fillSample(sample.text)}
                  className="px-3 py-2 md:px-4 md:py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 rounded-lg text-sm font-medium transition-all-fast border border-slate-600 touch-target"
                >
                  {sample.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
