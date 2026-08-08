import React from 'react';
import { Filter, Layers, Search } from 'lucide-react';

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
    <div className="bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-xl p-4 mb-6 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
      {/* Severity Filter Tabs */}
      <div className="flex flex-wrap items-center gap-1.5">
        <span className="text-xs text-[var(--text-secondary)] font-semibold mr-1 flex items-center gap-1">
          <Filter className="w-3.5 h-3.5 text-[var(--text-muted)]" />
          Severity:
        </span>
        {severities.map((sev) => (
          <button
            key={sev}
            onClick={() => onSelectSeverity(sev)}
            className={`px-2.5 py-1 rounded text-xs font-semibold tracking-wide transition-colors ${
              selectedSeverity === sev
                ? 'bg-[var(--accent-primary)] text-white shadow'
                : 'bg-[var(--bg-input)] hover:bg-[var(--hover-bg)] text-[var(--text-secondary)] border border-[var(--border-input)]'
            }`}
          >
            {sev}
          </button>
        ))}
      </div>

      {/* Category Filter Tabs */}
      <div className="flex flex-wrap items-center gap-1.5">
        <span className="text-xs text-[var(--text-secondary)] font-semibold mr-1 flex items-center gap-1">
          <Layers className="w-3.5 h-3.5 text-[var(--text-muted)]" />
          Category:
        </span>
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => onSelectCategory(cat)}
            className={`px-2.5 py-1 rounded text-xs font-medium transition-colors ${
              selectedCategory === cat
                ? 'bg-[var(--accent-primary)]/30 text-[var(--accent-primary-light)] border border-[var(--accent-primary)]/40'
                : 'bg-[var(--bg-input)] hover:bg-[var(--hover-bg)] text-[var(--text-secondary)] border border-[var(--border-input)]'
            }`}
          >
            {cat.replace('_', ' ')}
          </button>
        ))}
      </div>

      {/* File Search */}
      <div className="w-full md:w-48 relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-[var(--text-muted)]" />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => onSearchQueryChange(e.target.value)}
          placeholder="Filter by file path..."
          className="w-full pl-9 pr-3 py-1.5 bg-[var(--bg-input)] border border-[var(--border-input)] rounded text-xs text-[var(--text-primary)] placeholder-[var(--text-muted)] focus:border-[var(--accent-primary)] focus:outline-none"
        />
      </div>
    </div>
  );
};
