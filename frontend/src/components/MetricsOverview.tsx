import React from 'react';
import type { PRMetadata, SeverityBreakdown } from '../types/review';
import { GitPullRequest, GitCommit, FileCode } from 'lucide-react';

interface Props {
  metadata: PRMetadata;
  overallScore: number;
  summary: string;
  breakdown: SeverityBreakdown;
  findingsCount: number;
}

export const MetricsOverview: React.FC<Props> = ({
  metadata,
  overallScore,
  summary,
  breakdown,
  findingsCount,
}) => {
  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-emerald-400 border-emerald-500/40 bg-emerald-500/10';
    if (score >= 75) return 'text-blue-400 border-blue-500/40 bg-blue-500/10';
    if (score >= 50) return 'text-amber-400 border-amber-500/40 bg-amber-500/10';
    return 'text-rose-400 border-rose-500/40 bg-rose-500/10';
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 my-6">
      {/* PR Title & Metadata Banner */}
      <div className="lg:col-span-3 bg-gray-900/90 border border-gray-800 rounded-xl p-6 flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between gap-4 mb-2">
            <div className="flex items-center space-x-2">
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-gray-800 text-gray-300 border border-gray-700">
                {metadata.owner}/{metadata.repo} #{metadata.pr_number}
              </span>
              <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-medium">
                {metadata.state.toUpperCase()}
              </span>
            </div>
            <a
              href={metadata.html_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center space-x-1"
            >
              <span>View on GitHub</span>
              <GitPullRequest className="w-3.5 h-3.5" />
            </a>
          </div>

          <h1 className="text-xl font-bold text-white mb-2 leading-snug">{metadata.title}</h1>
          <p className="text-sm text-gray-400 mb-4">{summary}</p>
        </div>

        <div className="flex flex-wrap items-center gap-4 text-xs text-gray-400 border-t border-gray-800/80 pt-4">
          <div className="flex items-center space-x-1.5">
            <span className="text-gray-500">Author:</span>
            <span className="text-gray-200 font-medium">{metadata.author}</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <GitCommit className="w-3.5 h-3.5 text-gray-500" />
            <span className="text-gray-300 font-mono">{metadata.head_branch}</span>
            <span className="text-gray-600">→</span>
            <span className="text-gray-300 font-mono">{metadata.base_branch}</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <FileCode className="w-3.5 h-3.5 text-gray-500" />
            <span className="text-gray-300">{metadata.changed_files_count} files changed</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-emerald-400 font-mono">+{metadata.additions}</span>
            <span className="text-rose-400 font-mono">-{metadata.deletions}</span>
          </div>
        </div>
      </div>

      {/* Health Score & Severity Breakdown Card */}
      <div className="bg-gray-900/90 border border-gray-800 rounded-xl p-6 flex flex-col items-center justify-center text-center">
        <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Overall PR Health</span>
        
        <div className={`w-20 h-20 rounded-full border-2 flex items-center justify-center mb-3 ${getScoreColor(overallScore)} shadow-lg`}>
          <span className="text-2xl font-black tracking-tight">{overallScore}</span>
          <span className="text-xs font-bold text-gray-500 self-start mt-4">/100</span>
        </div>

        <div className="w-full flex items-center justify-between text-xs pt-3 border-t border-gray-800/80 mt-1">
          <span className="text-gray-400">Total Findings:</span>
          <span className="font-bold text-white bg-gray-800 px-2 py-0.5 rounded">{findingsCount}</span>
        </div>

        <div className="grid grid-cols-3 gap-1.5 w-full mt-3 text-[11px]">
          <div className="p-1.5 rounded bg-rose-500/10 border border-rose-500/20 text-rose-300">
            <div className="font-bold">{breakdown.CRITICAL}</div>
            <div className="text-[9px] uppercase tracking-wider text-rose-400/80">Critical</div>
          </div>
          <div className="p-1.5 rounded bg-amber-500/10 border border-amber-500/20 text-amber-300">
            <div className="font-bold">{breakdown.HIGH}</div>
            <div className="text-[9px] uppercase tracking-wider text-amber-400/80">High</div>
          </div>
          <div className="p-1.5 rounded bg-blue-500/10 border border-blue-500/20 text-blue-300">
            <div className="font-bold">{breakdown.MEDIUM}</div>
            <div className="text-[9px] uppercase tracking-wider text-blue-400/80">Medium</div>
          </div>
        </div>
      </div>
    </div>
  );
};
