import React, { useState } from 'react';
import type { Finding } from '../types/review';
import { SeverityBadge } from './SeverityBadge';
import { FileCode, AlertCircle, HelpCircle, Check, Copy, ChevronDown, ChevronUp } from 'lucide-react';

interface Props {
  finding: Finding;
}

export const FindingCard: React.FC<Props> = ({ finding }) => {
  const [copied, setCopied] = useState(false);
  const [isExpanded, setIsExpanded] = useState(true);

  const handleCopyCode = () => {
    navigator.clipboard.writeText(finding.suggested_fix);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const confidencePercent = Math.round(finding.confidence * 100);

  return (
    <div className="bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-xl overflow-hidden shadow-lg transition-all hover:border-[var(--border-highlight)]/80 mb-4">
      {/* Header Bar */}
      <div
        onClick={() => setIsExpanded(!isExpanded)}
        className="px-5 py-4 flex items-center justify-between cursor-pointer bg-[var(--bg-card)]/50 hover:bg-[var(--hover-bg)]/40 transition-colors border-b border-[var(--border-subtle)]/60"
      >
        <div className="flex items-center space-x-3 flex-1 min-w-0 pr-4">
          <SeverityBadge severity={finding.severity} />
          
          <span className="text-xs font-semibold uppercase tracking-wider px-2 py-0.5 rounded bg-[var(--bg-input)] text-[var(--text-secondary)] border border-[var(--border-input)]">
            {finding.category.replace('_', ' ')}
          </span>

          <span className="text-sm font-bold text-[var(--text-primary)] truncate">{finding.title}</span>
        </div>

        <div className="flex items-center space-x-4 flex-shrink-0">
          <div className="flex items-center space-x-1 font-mono text-xs text-[var(--accent-primary-light)] bg-[var(--bg-input)] px-2.5 py-1 rounded border border-[var(--border-input)]">
            <FileCode className="w-3.5 h-3.5 text-[var(--accent-primary-light)]" />
            <span className="truncate max-w-[200px]">{finding.file_path}</span>
            {finding.line_start && (
              <span className="text-[var(--accent-primary-light)] font-bold">
                :L{finding.line_start}{finding.line_end && finding.line_end !== finding.line_start ? `-L${finding.line_end}` : ''}
              </span>
            )}
          </div>

          <div className="hidden sm:flex items-center space-x-1 text-xs text-[var(--text-muted)]">
            <span className="text-[var(--text-muted)]">Conf:</span>
            <span className="font-semibold text-[var(--text-secondary)]">{confidencePercent}%</span>
          </div>

          <button className="text-[var(--text-muted)] hover:text-[var(--text-primary)] p-1">
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="p-5 space-y-4 bg-[var(--bg-card-hover)]/40">
          {/* Description */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[var(--text-muted)] mb-1 flex items-center gap-1.5">
              <AlertCircle className="w-3.5 h-3.5 text-[var(--accent-warning-light)]" />
              Issue Description
            </h4>
            <p className="text-sm text-[var(--text-primary)] leading-relaxed font-sans">{finding.description}</p>
          </div>

          {/* Why it Matters */}
          <div className="p-3.5 rounded-lg bg-[var(--bg-card)] border border-[var(--border-subtle)]">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-[var(--accent-primary-light)] mb-1 flex items-center gap-1.5">
              <HelpCircle className="w-3.5 h-3.5 text-[var(--accent-primary-light)]" />
              Why It Matters
            </h4>
            <p className="text-xs text-[var(--text-secondary)] leading-normal">{finding.why_it_matters}</p>
          </div>

          {/* Actionable Code Fix */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-[var(--accent-success-light)] flex items-center gap-1.5">
                <Check className="w-3.5 h-3.5 text-[var(--accent-success-light)]" />
                Suggested Fix / Recommendation
              </h4>
              <button
                onClick={handleCopyCode}
                className="flex items-center space-x-1 px-2.5 py-1 rounded bg-[var(--bg-input)] hover:bg-[var(--hover-bg)] text-xs text-[var(--text-secondary)] transition-colors border border-[var(--border-input)]"
              >
                {copied ? (
                  <>
                    <Check className="w-3 h-3 text-[var(--accent-success-light)]" />
                    <span className="text-[var(--accent-success-light)] font-semibold">Copied!</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-3 h-3 text-[var(--text-muted)]" />
                    <span>Copy Fix</span>
                  </>
                )}
              </button>
            </div>

            <div className="relative rounded-lg overflow-hidden border border-[var(--border-subtle)] bg-[var(--bg-input)] font-mono text-xs text-[var(--accent-success-light)] p-4 overflow-x-auto leading-relaxed shadow-inner">
              <pre><code>{finding.suggested_fix}</code></pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
