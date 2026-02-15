'use client';

import { Moon, Sun, Brain } from 'lucide-react';
import Sidebar from '../components/Sidebar';
import { useTheme } from '../contexts/ThemeContext';
import { useSettings } from '../contexts/SettingsContext';

export default function SettingsPage() {
  const { theme, toggleTheme } = useTheme();
  const { aiModel, setAIModel } = useSettings();

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white">
      <Sidebar />
      
      <main className="flex-1 p-8">
        <div className="max-w-4xl mx-auto space-y-6">
          <div>
            <h1 className="text-3xl font-bold mb-2 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              Settings
            </h1>
            <p className="text-slate-400">Customize your dashboard experience</p>
          </div>

          <div className="space-y-6">
            {/* Theme Toggle */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 shadow-lg p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  {theme === 'dark' ? (
                    <Moon className="text-blue-400" size={24} />
                  ) : (
                    <Sun className="text-yellow-400" size={24} />
                  )}
                  <div>
                    <h3 className="text-lg font-semibold text-white mb-1">Theme</h3>
                    <p className="text-sm text-slate-400">
                      Switch between dark and light mode
                    </p>
                  </div>
                </div>
                <button
                  onClick={toggleTheme}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    theme === 'dark' ? 'bg-blue-600' : 'bg-slate-600'
                  }`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                      theme === 'dark' ? 'translate-x-6' : 'translate-x-1'
                    }`}
                  />
                </button>
              </div>
              <div className="mt-4 pt-4 border-t border-slate-700/50">
                <p className="text-sm text-slate-400">
                  Current theme: <span className="text-white font-medium capitalize">{theme}</span>
                </p>
              </div>
            </div>

            {/* AI Model Selector */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 shadow-lg p-6">
              <div className="flex items-center gap-4 mb-4">
                <Brain className="text-purple-400" size={24} />
                <div>
                  <h3 className="text-lg font-semibold text-white mb-1">AI Model</h3>
                  <p className="text-sm text-slate-400">
                    Select the sentiment analysis model
                  </p>
                </div>
              </div>
              
              <div className="space-y-3">
                <label className="block">
                  <select
                    value={aiModel}
                    onChange={(e) => setAIModel(e.target.value as 'VADER (Fast)' | 'FinBERT (Accurate)')}
                    className="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  >
                    <option value="VADER (Fast)">VADER (Fast)</option>
                    <option value="FinBERT (Accurate)">FinBERT (Accurate)</option>
                  </select>
                </label>
                
                <div className="mt-4 pt-4 border-t border-slate-700/50">
                  <div className="space-y-2 text-sm">
                    <div className="flex items-start gap-2">
                      <span className="text-slate-400">•</span>
                      <span className="text-slate-300">
                        <strong className="text-white">VADER (Fast):</strong> Quick sentiment analysis using rule-based approach. Best for real-time processing.
                      </span>
                    </div>
                    <div className="flex items-start gap-2">
                      <span className="text-slate-400">•</span>
                      <span className="text-slate-300">
                        <strong className="text-white">FinBERT (Accurate):</strong> Deep learning model trained on financial texts. More accurate but slower.
                      </span>
                    </div>
                  </div>
                  <p className="mt-4 text-xs text-slate-500 italic">
                    Note: This is a UI placeholder. Model selection will be implemented in future updates.
                  </p>
                </div>
              </div>
            </div>

            {/* Additional Settings Placeholder */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700/50 shadow-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-4">About</h3>
              <div className="space-y-2 text-sm text-slate-400">
                <p>CryptoSentiment Dashboard v1.0</p>
                <p>Real-time cryptocurrency sentiment analysis powered by AI</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

