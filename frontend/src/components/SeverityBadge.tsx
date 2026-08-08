import React from 'react';
import type { Severity } from '../types/review';

interface Props {
  severity: Severity;
}

export const SeverityBadge: React.FC<Props> = ({ severity }) => {
  const getStyleClass = () => {
    switch (severity) {
      case 'CRITICAL':
        return 'severity-critical';
      case 'HIGH':
        return 'severity-high';
      case 'MEDIUM':
        return 'severity-medium';
      case 'LOW':
        return 'severity-low';
      case 'INFO':
      default:
        return 'severity-info';
    }
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold tracking-wide uppercase ${getStyleClass()}`}>
      {severity}
    </span>
  );
};
