import React from 'react';
import type { PRReviewResponse } from '../types/review';
import { ShieldCheck, ArrowRight } from 'lucide-react';

interface Props {
  recentReviews: PRReviewResponse[];
  onSelectReview: (review: PRReviewResponse) => void;
}

export const DashboardPage: React.FC<Props> = ({ recentReviews, onSelectReview }) => {
  const getScoreBadgeClass = (score: number) => {
    if (score >= 90) return 'bg-[var(--accent-success)]/10 text-[var(--accent-success-light)] border-[var(--accent-success)]/30';
    if (score >= 75) return 'bg-[var(--accent-info)]/10 text-[var(--accent-info-light)] border-[var(--accent-info)]/30';
    if (score >= 50) return 'bg-[var(--accent-warning)]/10 text-[var(--accent-warning-light)] border-[var(--accent-warning)]/30';
    return 'bg-[var(--accent-danger)]/10 text-[var(--accent-danger-light)] border-[var(--accent-danger)]/30';
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-[var(--text-primary)] tracking-tight">Recent PR Reviews</h2>
          <p className="text-xs text-[var(--text-secondary)]">History of analyzed pull requests across connected repositories</p>
        </div>
      </div>

      {recentReviews.length === 0 ? (
        <div className="bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-xl p-12 text-center">
          <ShieldCheck className="w-12 h-12 text-[var(--text-muted)] mx-auto mb-3" />
          <h3 className="text-base font-semibold text-[var(--text-secondary)] mb-1">No Reviews Analyzed Yet</h3>
          <p className="text-xs text-[var(--text-muted)] max-w-md mx-auto">
            Paste a GitHub Pull Request URL above or load a sample PR to trigger the multi-agent AI review pipeline.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {recentReviews.map((review) => (
            <div
              key={review.id}
              onClick={() => onSelectReview(review)}
              className="bg-[var(--bg-card)] border border-[var(--border-subtle)] hover:border-[var(--accent-primary)]/50 rounded-xl p-5 cursor-pointer transition-all hover:shadow-xl group"
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <span className="text-xs font-mono px-2 py-0.5 rounded bg-[var(--bg-input)] text-[var(--text-secondary)] border border-[var(--border-input)]">
                    {review.pr_metadata.owner}/{review.pr_metadata.repo} #{review.pr_metadata.pr_number}
                  </span>
                  <h3 className="text-sm font-bold text-[var(--text-primary)] mt-2 group-hover:text-[var(--accent-primary-light)] transition-colors line-clamp-1">
                    {review.pr_metadata.title}
                  </h3>
                </div>

                <div className={`px-2.5 py-1 rounded-full border text-xs font-bold ${getScoreBadgeClass(review.overall_score)}`}>
                  {review.overall_score} Score
                </div>
              </div>

              <p className="text-xs text-[var(--text-secondary)] line-clamp-2 mb-4">{review.summary}</p>

              <div className="flex items-center justify-between pt-3 border-t border-[var(--border-subtle)]/80 text-xs text-[var(--text-muted)]">
                <div className="flex items-center space-x-3">
                  <span>Author: <strong className="text-[var(--text-primary)] font-medium">{review.pr_metadata.author}</strong></span>
                  <span>Findings: <strong className="text-[var(--text-primary)]">{review.findings_count}</strong></span>
                </div>
                <div className="flex items-center space-x-1 text-[var(--accent-primary-light)] group-hover:translate-x-1 transition-transform">
                  <span>View Details</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
