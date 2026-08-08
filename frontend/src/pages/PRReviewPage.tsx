import React, { useState, useMemo } from 'react';
import type { PRReviewResponse } from '../types/review';
import { MetricsOverview } from '../components/MetricsOverview';
import { FilterBar } from '../components/FilterBar';
import { FindingCard } from '../components/FindingCard';
import { ShieldCheck, ArrowLeft } from 'lucide-react';

interface Props {
  review: PRReviewResponse;
  onBack: () => void;
}

export const PRReviewPage: React.FC<Props> = ({ review, onBack }) => {
  const [selectedSeverity, setSelectedSeverity] = useState('ALL');
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredFindings = useMemo(() => {
    return review.findings.filter((f) => {
      const matchSeverity = selectedSeverity === 'ALL' || f.severity === selectedSeverity;
      const matchCategory = selectedCategory === 'ALL' || f.category === selectedCategory;
      const matchSearch =
        !searchQuery.trim() ||
        f.file_path.toLowerCase().includes(searchQuery.toLowerCase()) ||
        f.title.toLowerCase().includes(searchQuery.toLowerCase());

      return matchSeverity && matchCategory && matchSearch;
    });
  }, [review.findings, selectedSeverity, selectedCategory, searchQuery]);

  return (
    <div>
      <div className="flex items-center space-x-2 mb-2">
        <button
          onClick={onBack}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-gray-900 hover:bg-gray-800 border border-gray-800 text-xs text-gray-300 font-medium transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Dashboard</span>
        </button>
      </div>

      <MetricsOverview
        metadata={review.pr_metadata}
        overallScore={review.overall_score}
        summary={review.summary}
        breakdown={review.severity_breakdown}
        findingsCount={review.findings_count}
      />

      <FilterBar
        selectedSeverity={selectedSeverity}
        onSelectSeverity={setSelectedSeverity}
        selectedCategory={selectedCategory}
        onSelectCategory={setSelectedCategory}
        searchQuery={searchQuery}
        onSearchQueryChange={setSearchQuery}
      />

      <div className="space-y-4">
        {filteredFindings.length === 0 ? (
          <div className="bg-gray-900/60 border border-gray-800 rounded-xl p-12 text-center">
            <ShieldCheck className="w-10 h-10 text-emerald-400 mx-auto mb-2" />
            <h3 className="text-base font-semibold text-gray-300">No Findings Match Current Filters</h3>
            <p className="text-xs text-gray-500 mt-1">Try resetting severity or category filters to view all findings.</p>
          </div>
        ) : (
          filteredFindings.map((finding, idx) => (
            <FindingCard key={finding.id || idx} finding={finding} />
          ))
        )}
      </div>
    </div>
  );
};
