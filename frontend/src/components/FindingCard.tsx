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
    <div className="bg-gray-900/90 border border-gray-800 rounded-xl overflow-hidden shadow-lg transition-all hover:border-gray-700/80 mb-4">
      {/* Header Bar */}
      <div
        onClick={() => setIsExpanded(!isExpanded)}
        className="px-5 py-4 flex items-center justify-between cursor-pointer bg-gray-900/50 hover:bg-gray-800/40 transition-colors border-b border-gray-800/60"
      >
        <div className="flex items-center space-x-3 flex-1 min-w-0 pr-4">
          <SeverityBadge severity={finding.severity} />
          
          <span className="text-xs font-semibold uppercase tracking-wider px-2 py-0.5 rounded bg-gray-800 text-gray-300 border border-gray-700">
            {finding.category.replace('_', ' ')}
          </span>

          <span className="text-sm font-bold text-white truncate">{finding.title}</span>
        </div>

        <div className="flex items-center space-x-4 flex-shrink-0">
          <div className="flex items-center space-x-1 font-mono text-xs text-indigo-300 bg-gray-950 px-2.5 py-1 rounded border border-gray-800">
            <FileCode className="w-3.5 h-3.5 text-indigo-400" />
            <span className="truncate max-w-[200px]">{finding.file_path}</span>
            {finding.line_start && (
              <span className="text-indigo-400 font-bold">
                :L{finding.line_start}{finding.line_end && finding.line_end !== finding.line_start ? `-L${finding.line_end}` : ''}
              </span>
            )}
          </div>

          <div className="hidden sm:flex items-center space-x-1 text-xs text-gray-400">
            <span className="text-gray-500">Conf:</span>
            <span className="font-semibold text-gray-200">{confidencePercent}%</span>
          </div>

          <button className="text-gray-400 hover:text-white p-1">
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="p-5 space-y-4 bg-gray-950/40">
          {/* Description */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-wider text-gray-400 mb-1 flex items-center gap-1.5">
              <AlertCircle className="w-3.5 h-3.5 text-amber-400" />
              Issue Description
            </h4>
            <p className="text-sm text-gray-200 leading-relaxed font-sans">{finding.description}</p>
          </div>

          {/* Why it Matters */}
          <div className="p-3.5 rounded-lg bg-gray-900/80 border border-gray-800">
            <h4 className="text-xs font-semibold uppercase tracking-wider text-indigo-300 mb-1 flex items-center gap-1.5">
              <HelpCircle className="w-3.5 h-3.5 text-indigo-400" />
              Why It Matters
            </h4>
            <p className="text-xs text-gray-300 leading-normal">{finding.why_it_matters}</p>
          </div>

          {/* Actionable Code Fix */}
          <div>
            <div className="flex items-center justify-between mb-1.5">
              <h4 className="text-xs font-semibold uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                Suggested Fix / Recommendation
              </h4>
              <button
                onClick={handleCopyCode}
                className="flex items-center space-x-1 px-2.5 py-1 rounded bg-gray-800 hover:bg-gray-700 text-xs text-gray-300 transition-colors border border-gray-700"
              >
                {copied ? (
                  <>
                    <Check className="w-3 h-3 text-emerald-400" />
                    <span className="text-emerald-400 font-semibold">Copied!</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-3 h-3 text-gray-400" />
                    <span>Copy Fix</span>
                  </>
                )}
              </button>
            </div>

            <div className="relative rounded-lg overflow-hidden border border-gray-800 bg-gray-950 font-mono text-xs text-emerald-300 p-4 overflow-x-auto leading-relaxed shadow-inner">
              <pre><code>{finding.suggested_fix}</code></pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
