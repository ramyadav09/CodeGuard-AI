import React from 'react';
import { ShieldCheck, Cpu, GitPullRequest, Activity } from 'lucide-react';

interface Props {
  isHealthy: boolean;
  activeProvider: string;
}

export const Navbar: React.FC<Props> = ({ isHealthy, activeProvider }) => {
  return (
    <header className="border-b border-gray-800 bg-gray-950/80 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-indigo-600/20 rounded-lg border border-indigo-500/30 text-indigo-400">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg tracking-tight text-white">CodeGuard AI</span>
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                Track B: Productivity
              </span>
            </div>
            <p className="text-xs text-gray-400 hidden sm:block">AI-Powered PR Review & Risk Inspection</p>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="hidden md:flex items-center space-x-2 px-3 py-1 rounded-full bg-gray-900 border border-gray-800 text-xs text-gray-300">
            <Cpu className="w-3.5 h-3.5 text-indigo-400" />
            <span className="text-gray-400">Engine:</span>
            <span className="font-mono text-indigo-300 uppercase font-semibold">{activeProvider}</span>
          </div>

          <div className="flex items-center space-x-2 px-3 py-1 rounded-full bg-gray-900 border border-gray-800 text-xs">
            <Activity className={`w-3.5 h-3.5 ${isHealthy ? 'text-emerald-400 animate-pulse' : 'text-rose-400'}`} />
            <span className="text-gray-300 font-medium">
              {isHealthy ? 'Backend Ready' : 'Connecting...'}
            </span>
          </div>

          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-1 px-3 py-1.5 rounded-md bg-gray-900 hover:bg-gray-800 border border-gray-800 text-xs text-gray-300 font-medium transition-colors"
          >
            <GitPullRequest className="w-3.5 h-3.5 text-gray-400" />
            <span className="hidden sm:inline">GitHub</span>
          </a>
        </div>
      </div>
    </header>
  );
};
