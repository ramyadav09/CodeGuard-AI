import { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { PRInputForm } from './components/PRInputForm';
import { DashboardPage } from './pages/DashboardPage';
import { PRReviewPage } from './pages/PRReviewPage';
import type { PRReviewRequest, PRReviewResponse } from './types/review';
import { apiService } from './services/api';
import { ShieldCheck, AlertCircle } from 'lucide-react';
import { ThemeProvider } from './context/ThemeContext';

export function App() {
  const [isHealthy, setIsHealthy] = useState(false);
  const [activeProvider, setActiveProvider] = useState('mock');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [activeReview, setActiveReview] = useState<PRReviewResponse | null>(null);
  const [recentReviews, setRecentReviews] = useState<PRReviewResponse[]>([]);

  useEffect(() => {
    checkHealth();
    loadRecentReviews();
  }, []);

  const checkHealth = async () => {
    try {
      const data = await apiService.getHealth();
      setIsHealthy(data.status === 'healthy');
      if (data.ai_provider) {
        setActiveProvider(data.ai_provider);
      }
    } catch {
      setIsHealthy(false);
    }
  };

  const loadRecentReviews = async () => {
    try {
      const data = await apiService.getRecentReviews();
      setRecentReviews(data);
    } catch {
      // Backend offline initially
    }
  };

  const handleAnalyze = async (payload: PRReviewRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const review = await apiService.analyzePR(payload);
      setActiveReview(review);
      setRecentReviews((prev) => [review, ...prev.filter((r) => r.id !== review.id)]);
    } catch (err: any) {
      const detail = err.response?.data?.detail || err.message || 'Failed to analyze pull request.';
      setError(detail);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-[var(--bg-main)] text-[var(--text-primary)] flex flex-col font-sans">
        <Navbar isHealthy={isHealthy} activeProvider={activeProvider} />

        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
          <PRInputForm onAnalyze={handleAnalyze} isLoading={isLoading} />

          {error && (
            <div className="p-4 rounded-xl bg-[var(--accent-danger)]/10 border border-[var(--accent-danger)]/30 text-[var(--accent-danger-light)] flex items-center space-x-3 text-sm">
              <AlertCircle className="w-5 h-5 flex-shrink-0 text-[var(--accent-danger)]" />
              <div className="flex-1">{error}</div>
            </div>
          )}

          {activeReview ? (
            <PRReviewPage review={activeReview} onBack={() => setActiveReview(null)} />
          ) : (
            <DashboardPage
              recentReviews={recentReviews}
              onSelectReview={(rev) => setActiveReview(rev)}
            />
          )}
        </main>

        <footer className="border-t border-[var(--border-subtle)] bg-[var(--footer-bg)] py-6 text-center text-xs text-[var(--text-muted)]">
          <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
            <div className="flex items-center space-x-2">
              <ShieldCheck className="w-4 h-4 text-[var(--accent-primary)]" />
              <span className="font-semibold text-[var(--text-secondary)]">CodeGuard AI</span>
              <span>— Track B Developer Productivity Platform</span>
            </div>
            <div>HowToAlgo x GDG on Campus KIIT Hackathon</div>
          </div>
        </footer>
      </div>
    </ThemeProvider>
  );
}

export default App;
