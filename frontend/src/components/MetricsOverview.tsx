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
    if (score >= 90) return 'text-[var(--accent-success-light)] border-[var(--accent-success)]/40 bg-[var(--accent-success)]/10';
    if (score >= 75) return 'text-[var(--accent-info-light)] border-[var(--accent-info)]/40 bg-[var(--accent-info)]/10';
    if (score >= 50) return 'text-[var(--accent-warning-light)] border-[var(--accent-warning)]/40 bg-[var(--accent-warning)]/10';
    return 'text-[var(--accent-danger-light)] border-[var(--accent-danger)]/40 bg-[var(--accent-danger)]/10';
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 my-6">
      {/* PR Title & Metadata Banner */}
      <div className="lg:col-span-3 bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-xl p-6 flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between gap-4 mb-2">
            <div className="flex items-center space-x-2">
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-[var(--bg-input)] text-[var(--text-secondary)] border border-[var(--border-input)]">
                {metadata.owner}/{metadata.repo} #{metadata.pr_number}
              </span>
              <span className="text-xs px-2 py-0.5 rounded bg-[var(--accent-success)]/10 text-[var(--accent-success-light)] border border-[var(--accent-success)]/30 font-medium">
                {metadata.state.toUpperCase()}
              </span>
            </div>
            <a
              href={metadata.html_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-[var(--accent-primary-light)] hover:text-[var(--accent-primary)] flex items-center space-x-1"
            >
              <span>View on GitHub</span>
              <GitPullRequest className="w-3.5 h-3.5" />
            </a>
          </div>

          <h1 className="text-xl font-bold text-[var(--text-primary)] mb-2 leading-snug">{metadata.title}</h1>
          <p className="text-sm text-[var(--text-secondary)] mb-4">{summary}</p>
        </div>

        <div className="flex flex-wrap items-center gap-4 text-xs text-[var(--text-secondary)] border-t border-[var(--border-subtle)]/80 pt-4">
          <div className="flex items-center space-x-1.5">
            <span className="text-[var(--text-muted)]">Author:</span>
            <span className="text-[var(--text-primary)] font-medium">{metadata.author}</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <GitCommit className="w-3.5 h-3.5 text-[var(--text-muted)]" />
            <span className="text-[var(--text-primary)] font-mono">{metadata.head_branch}</span>
            <span className="text-[var(--text-muted)]">→</span>
            <span className="text-[var(--text-primary)] font-mono">{metadata.base_branch}</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <FileCode className="w-3.5 h-3.5 text-[var(--text-muted)]" />
            <span className="text-[var(--text-primary)]">{metadata.changed_files_count} files changed</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-[var(--accent-success-light)] font-mono">+{metadata.additions}</span>
            <span className="text-[var(--accent-danger-light)] font-mono">-{metadata.deletions}</span>
          </div>
        </div>
      </div>

      {/* Health Score & Severity Breakdown Card */}
      <div className="bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-xl p-6 flex flex-col items-center justify-center text-center">
        <span className="text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider mb-2">Overall PR Health</span>
        
        <div className={`w-20 h-20 rounded-full border-2 flex items-center justify-center mb-3 ${getScoreColor(overallScore)} shadow-lg`}>
          <span className="text-2xl font-black tracking-tight">{overallScore}</span>
          <span className="text-xs font-bold text-[var(--text-muted)] self-start mt-4">/100</span>
        </div>

        <div className="w-full flex items-center justify-between text-xs pt-3 border-t border-[var(--border-subtle)]/80 mt-1">
          <span className="text-[var(--text-secondary)]">Total Findings:</span>
          <span className="font-bold text-[var(--text-primary)] bg-[var(--bg-input)] px-2 py-0.5 rounded">{findingsCount}</span>
        </div>

        <div className="grid grid-cols-3 gap-1.5 w-full mt-3 text-[11px]">
          <div className="p-1.5 rounded bg-[var(--severity-critical-bg)] border border-[var(--severity-critical-border)] text-[var(--severity-critical-color)]">
            <div className="font-bold">{breakdown.CRITICAL}</div>
            <div className="text-[9px] uppercase tracking-wider text-[var(--severity-critical-color)]/80">Critical</div>
          </div>
          <div className="p-1.5 rounded bg-[var(--severity-high-bg)] border border-[var(--severity-high-border)] text-[var(--severity-high-color)]">
            <div className="font-bold">{breakdown.HIGH}</div>
            <div className="text-[9px] uppercase tracking-wider text-[var(--severity-high-color)]/80">High</div>
          </div>
          <div className="p-1.5 rounded bg-[var(--severity-medium-bg)] border border-[var(--severity-medium-border)] text-[var(--severity-medium-color)]">
            <div className="font-bold">{breakdown.MEDIUM}</div>
            <div className="text-[9px] uppercase tracking-wider text-[var(--severity-medium-color)]/80">Medium</div>
          </div>
        </div>
      </div>
    </div>
  );
};
