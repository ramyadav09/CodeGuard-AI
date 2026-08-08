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
    <div className="bg-gray-900/90 border border-gray-800 rounded-xl p-6 shadow-2xl backdrop-blur-md">
      <div className="flex items-center space-x-2 mb-4">
        <Sparkles className="w-5 h-5 text-indigo-400" />
        <h2 className="text-lg font-semibold text-white tracking-tight">Analyze Pull Request</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="relative flex-1">
            <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-500">
              <Search className="w-4 h-4" />
            </div>
            <input
              type="text"
              value={prUrl}
              onChange={(e) => setPrUrl(e.target.value)}
              placeholder="Paste GitHub PR URL e.g. https://github.com/owner/repo/pull/123"
              className="w-full pl-10 pr-4 py-3 bg-gray-950 border border-gray-800 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 rounded-lg text-sm text-gray-100 placeholder-gray-500 transition-colors"
              disabled={isLoading}
            />
          </div>

          <select
            value={aiProvider}
            onChange={(e) => setAiProvider(e.target.value)}
            className="bg-gray-950 border border-gray-800 focus:border-indigo-500 rounded-lg px-3 py-3 text-sm text-gray-200"
            disabled={isLoading}
          >
            <option value="gemini">Google Gemini AI</option>
            <option value="nvidia">Nvidia NIM AI</option>
            <option value="mock">Offline Mock AI (Deterministic)</option>
          </select>

          <button
            type="submit"
            disabled={isLoading}
            className="flex items-center justify-center space-x-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 font-medium text-sm text-white rounded-lg transition-colors shadow-lg shadow-indigo-600/20 disabled:opacity-50 disabled:cursor-not-allowed"
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
          <div className="flex items-center space-x-2 text-rose-400 text-xs mt-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <div className="pt-2 flex flex-wrap items-center gap-2">
          <span className="text-xs text-gray-500 font-medium">Quick Load Sample PRs:</span>
          {samplePRs.map((sample, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSelectSample(sample.url)}
              disabled={isLoading}
              className="px-2.5 py-1 bg-gray-800/60 hover:bg-gray-800 text-gray-300 rounded text-xs border border-gray-700/50 transition-colors"
            >
              {sample.label}
            </button>
          ))}
        </div>
      </form>
    </div>
  );
};
