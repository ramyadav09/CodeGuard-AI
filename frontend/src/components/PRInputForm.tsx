import React, { useState } from 'react';
import { Search, Loader2, Sparkles, AlertCircle } from 'lucide-react';
import type { PRReviewRequest } from '../types/review';

interface Props {
  onAnalyze: (payload: PRReviewRequest) => void;
  isLoading: boolean;
}

export const PRInputForm: React.FC<Props> = ({ onAnalyze, isLoading }) => {
  const [prUrl, setPrUrl] = useState('');
  const [aiProvider, setAiProvider] = useState('gemini');
  const [error, setError] = useState('');

  const samplePRs = [
    { label: 'octocat/Hello-World #1', url: 'https://github.com/octocat/Hello-World/pull/1' },
    { label: 'facebook/react #1024', url: 'https://github.com/facebook/react/pull/1024' },
    { label: 'pallets/flask #5000', url: 'https://github.com/pallets/flask/pull/5000' }
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!prUrl.trim()) {
      setError('Please enter a GitHub Pull Request URL');
      return;
    }
    setError('');
    onAnalyze({ repo_url: prUrl.trim(), ai_provider: aiProvider });
  };

  const handleSelectSample = (url: string) => {
    setPrUrl(url);
    setError('');
    onAnalyze({ repo_url: url, ai_provider: aiProvider });
  };

  return (
    <div className="bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-xl p-6 shadow-2xl backdrop-blur-md">
      <div className="flex items-center space-x-2 mb-4">
        <Sparkles className="w-5 h-5 text-[var(--accent-primary-light)]" />
        <h2 className="text-lg font-semibold text-[var(--text-primary)] tracking-tight">Analyze Pull Request</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="relative flex-1">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-[var(--text-muted)]">
              <Search className="w-4 h-4" />
            </div>
            <input
              type="text"
              value={prUrl}
              onChange={(e) => setPrUrl(e.target.value)}
              placeholder="Paste GitHub PR URL e.g. https://github.com/owner/repo/pull/123"
              className="w-full pl-10 pr-4 py-3 bg-[var(--bg-input)] border border-[var(--border-input)] focus:border-[var(--accent-primary)] focus:ring-1 focus:ring-[var(--accent-primary)] rounded-lg text-sm text-[var(--text-primary)] placeholder-[var(--text-muted)] transition-colors"
              disabled={isLoading}
            />
          </div>

          <select
            value={aiProvider}
            onChange={(e) => setAiProvider(e.target.value)}
            className="bg-[var(--bg-input)] border border-[var(--border-input)] focus:border-[var(--accent-primary)] rounded-lg px-3 py-3 text-sm text-[var(--text-primary)]"
            disabled={isLoading}
          >
            <option value="gemini">Google Gemini AI</option>
            <option value="nvidia">Nvidia NIM AI</option>
            <option value="mock">Offline Mock AI (Deterministic)</option>
          </select>

          <button
            type="submit"
            disabled={isLoading}
            className="flex items-center justify-center space-x-2 px-6 py-3 bg-[var(--accent-primary)] hover:bg-[var(--accent-primary-hover)] active:bg-[var(--accent-primary)] font-medium text-sm text-white rounded-lg transition-colors shadow-lg shadow-[var(--accent-primary)]/20 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-white" />
                <span>Running Pipeline...</span>
              </>
            ) : (
              <span>Start AI Review</span>
            )}
          </button>
        </div>

        {error && (
          <div className="flex items-center space-x-2 text-[var(--accent-danger-light)] text-xs mt-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0 text-[var(--accent-danger)]" />
            <span>{error}</span>
          </div>
        )}

        <div className="pt-2 flex flex-wrap items-center gap-2">
          <span className="text-xs text-[var(--text-muted)] font-medium">Quick Load Sample PRs:</span>
          {samplePRs.map((sample, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSelectSample(sample.url)}
              disabled={isLoading}
              className="px-2.5 py-1 bg-[var(--bg-input)] hover:bg-[var(--hover-bg)] text-[var(--text-secondary)] rounded text-xs border border-[var(--border-input)]/50 transition-colors"
            >
              {sample.label}
            </button>
          ))}
        </div>
      </form>
    </div>
  );
};
