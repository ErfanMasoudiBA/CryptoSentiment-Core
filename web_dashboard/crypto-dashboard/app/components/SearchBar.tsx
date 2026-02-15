'use client';

import { Search, X } from 'lucide-react';
import { useState } from 'react';

interface SearchBarProps {
  onSearch: (query: string) => void;
  selectedCoin: string;
}

const popularCoins = [
  'All',
  'Bitcoin',
  'Ethereum',
  'Ripple',
  'Litecoin',
  'Dogecoin',
  'Cardano',
  'Solana',
  'Polkadot',
  'Chainlink',
];

export default function SearchBar({ onSearch, selectedCoin }: SearchBarProps) {
  const [searchQuery, setSearchQuery] = useState(selectedCoin === 'All' ? '' : selectedCoin);
  const [showDropdown, setShowDropdown] = useState(false);

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    onSearch(query === 'All' ? '' : query);
    setShowDropdown(false);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchQuery(value);
    if (value.trim()) {
      onSearch(value);
    } else {
      onSearch('');
    }
  };

  const clearSearch = () => {
    setSearchQuery('');
    onSearch('');
  };

  return (
    <div className="relative z-50">
      <div className="relative">
        <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
        <input
          type="text"
          value={searchQuery}
          onChange={handleInputChange}
          onFocus={() => setShowDropdown(true)}
          placeholder="Search by coin name (e.g., Bitcoin, Ethereum)..."
          className="w-full pl-12 pr-12 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
        />
        {searchQuery && (
          <button
            onClick={clearSearch}
            className="absolute right-4 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-white transition-colors"
          >
            <X size={18} />
          </button>
        )}
      </div>

      {showDropdown && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setShowDropdown(false)}
          />
          <div className="absolute top-full mt-2 w-full bg-slate-800 border border-slate-700 rounded-lg shadow-2xl z-50 max-h-64 overflow-y-auto">
            <div className="p-2">
              <div className="text-xs text-slate-400 px-3 py-2 font-semibold">Popular Coins</div>
              {popularCoins.map((coin) => (
                <button
                  key={coin}
                  onClick={() => handleSearch(coin)}
                  className={`w-full text-left px-4 py-2 rounded-md hover:bg-slate-700 transition-colors ${
                    selectedCoin === coin || (coin === 'All' && !selectedCoin)
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-300'
                  }`}
                >
                  {coin}
                </button>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

