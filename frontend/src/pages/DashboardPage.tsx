import React from 'react';
import type { PRReviewResponse } from '../types/review';
import { ShieldCheck, ArrowRight } from 'lucide-react';

interface Props {
  recentReviews: PRReviewResponse[];
  onSelectReview: (review: PRReviewResponse) => void;
}

export const DashboardPage: React.FC<Props> = ({ recentReviews, onSelectReview }) => {
  const getScoreBadgeClass = (score: number) => {
    if (score >= 90) return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
    if (score >= 75) return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
    if (score >= 50) return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
    return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-white tracking-tight">Recent PR Reviews</h2>
          <p className="text-xs text-gray-400">History of analyzed pull requests across connected repositories</p>
        </div>
      </div>

      {recentReviews.length === 0 ? (
        <div className="bg-gray-900/60 border border-gray-800 rounded-xl p-12 text-center">
          <ShieldCheck className="w-12 h-12 text-gray-600 mx-auto mb-3" />
          <h3 className="text-base font-semibold text-gray-300 mb-1">No Reviews Analyzed Yet</h3>
          <p className="text-xs text-gray-500 max-w-md mx-auto">
            Paste a GitHub Pull Request URL above or load a sample PR to trigger the multi-agent AI review pipeline.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {recentReviews.map((review) => (
            <div
              key={review.id}
              onClick={() => onSelectReview(review)}
              className="bg-gray-900/80 border border-gray-800 hover:border-indigo-500/50 rounded-xl p-5 cursor-pointer transition-all hover:shadow-xl group"
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <span className="text-xs font-mono px-2 py-0.5 rounded bg-gray-800 text-gray-300 border border-gray-700">
                    {review.pr_metadata.owner}/{review.pr_metadata.repo} #{review.pr_metadata.pr_number}
                  </span>
                  <h3 className="text-sm font-bold text-white mt-2 group-hover:text-indigo-300 transition-colors line-clamp-1">
                    {review.pr_metadata.title}
                  </h3>
                </div>

                <div className={`px-2.5 py-1 rounded-full border text-xs font-bold ${getScoreBadgeClass(review.overall_score)}`}>
                  {review.overall_score} Score
                </div>
              </div>

              <p className="text-xs text-gray-400 line-clamp-2 mb-4">{review.summary}</p>

              <div className="flex items-center justify-between pt-3 border-t border-gray-800/80 text-xs text-gray-500">
                <div className="flex items-center space-x-3">
                  <span>Author: <strong className="text-gray-300 font-medium">{review.pr_metadata.author}</strong></span>
                  <span>Findings: <strong className="text-white">{review.findings_count}</strong></span>
                </div>
                <div className="flex items-center space-x-1 text-indigo-400 group-hover:translate-x-1 transition-transform">
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
