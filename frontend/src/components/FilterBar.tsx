import React from 'react';
import { Filter, Layers } from 'lucide-react';

interface Props {
  selectedSeverity: string;
  onSelectSeverity: (sev: string) => void;
  selectedCategory: string;
  onSelectCategory: (cat: string) => void;
  searchQuery: string;
  onSearchQueryChange: (q: string) => void;
}

export const FilterBar: React.FC<Props> = ({
  selectedSeverity,
  onSelectSeverity,
  selectedCategory,
  onSelectCategory,
  searchQuery,
  onSearchQueryChange,
}) => {
  const severities = ['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'];
  const categories = ['ALL', 'BUG', 'SECURITY', 'CODE_QUALITY', 'TESTING', 'PERFORMANCE'];

  return (
    <div className="bg-gray-900/90 border border-gray-800 rounded-xl p-4 mb-6 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
      {/* Severity Filter Tabs */}
      <div className="flex flex-wrap items-center gap-1.5">
        <span className="text-xs text-gray-400 font-semibold mr-1 flex items-center gap-1">
          <Filter className="w-3.5 h-3.5 text-gray-500" />
          Severity:
        </span>
        {severities.map((sev) => (
          <button
            key={sev}
            onClick={() => onSelectSeverity(sev)}
            className={`px-2.5 py-1 rounded text-xs font-semibold tracking-wide transition-colors ${
              selectedSeverity === sev
                ? 'bg-indigo-600 text-white shadow'
                : 'bg-gray-800/80 hover:bg-gray-800 text-gray-400'
            }`}
          >
            {sev}
          </button>
        ))}
      </div>

      {/* Category Filter Tabs */}
      <div className="flex flex-wrap items-center gap-1.5">
        <span className="text-xs text-gray-400 font-semibold mr-1 flex items-center gap-1">
          <Layers className="w-3.5 h-3.5 text-gray-500" />
          Category:
        </span>
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => onSelectCategory(cat)}
            className={`px-2.5 py-1 rounded text-xs font-medium transition-colors ${
              selectedCategory === cat
                ? 'bg-indigo-600/30 text-indigo-300 border border-indigo-500/40'
                : 'bg-gray-800/60 hover:bg-gray-800 text-gray-400 border border-transparent'
            }`}
          >
            {cat.replace('_', ' ')}
          </button>
        ))}
      </div>

      {/* File Search */}
      <div className="w-full md:w-48">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => onSearchQueryChange(e.target.value)}
          placeholder="Filter by file path..."
          className="w-full px-3 py-1.5 bg-gray-950 border border-gray-800 rounded text-xs text-gray-200 placeholder-gray-500 focus:border-indigo-500 focus:outline-none"
        />
      </div>
    </div>
  );
};
