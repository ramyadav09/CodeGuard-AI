import React from 'react';
import { ShieldCheck, Cpu, GitPullRequest, Activity, Sun, Moon } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

interface Props {
  isHealthy: boolean;
  activeProvider: string;
}

export const Navbar: React.FC<Props> = ({ isHealthy, activeProvider }) => {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="border-b border-[var(--border-subtle)] bg-[var(--navbar-bg)] backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-[var(--accent-primary)]/20 rounded-lg border border-[var(--accent-primary)]/30 text-[var(--accent-primary-light)]">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg tracking-tight text-[var(--text-primary)]">CodeGuard AI</span>
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-[var(--accent-primary)]/20 text-[var(--accent-primary-light)] border border-[var(--accent-primary)]/30">
                Track B: Productivity
              </span>
            </div>
            <p className="text-xs text-[var(--text-muted)] hidden sm:block">AI-Powered PR Review & Risk Inspection</p>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="hidden md:flex items-center space-x-2 px-3 py-1 rounded-full bg-[var(--bg-card)] border border-[var(--border-subtle)] text-xs text-[var(--text-secondary)]">
            <Cpu className="w-3.5 h-3.5 text-[var(--accent-primary-light)]" />
            <span className="text-[var(--text-secondary)]">Engine:</span>
            <span className="font-mono text-[var(--accent-primary-light)] uppercase font-semibold">{activeProvider}</span>
          </div>

          <div className="flex items-center space-x-2 px-3 py-1 rounded-full bg-[var(--bg-card)] border border-[var(--border-subtle)] text-xs">
            <Activity className={`w-3.5 h-3.5 ${isHealthy ? 'text-[var(--accent-success)] animate-pulse' : 'text-[var(--accent-danger)]'}`} />
            <span className="text-[var(--text-secondary)] font-medium">
              {isHealthy ? 'Backend Ready' : 'Connecting...'}
            </span>
          </div>

          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg bg-[var(--bg-card)] hover:bg-[var(--hover-bg)] border border-[var(--border-subtle)] text-[var(--text-secondary)] transition-colors"
            aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>

          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-1 px-3 py-1.5 rounded-md bg-[var(--bg-card)] hover:bg-[var(--hover-bg)] border border-[var(--border-subtle)] text-xs text-[var(--text-secondary)] font-medium transition-colors"
          >
            <GitPullRequest className="w-3.5 h-3.5 text-[var(--text-muted)]" />
            <span className="hidden sm:inline">GitHub</span>
          </a>
        </div>
      </div>
    </header>
  );
};
