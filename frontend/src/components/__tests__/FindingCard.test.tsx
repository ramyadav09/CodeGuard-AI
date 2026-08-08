import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { FindingCard } from '../FindingCard';
import type { Finding } from '../../types/review';

const mockFinding: Finding = {
  id: 'finding-1',
  severity: 'CRITICAL',
  category: 'SECURITY',
  file_path: 'backend/app/core/config.py',
  line_start: 14,
  line_end: 18,
  title: 'Hardcoded Credentials Risk',
  description: 'Fallback API token detected in configuration settings default value.',
  why_it_matters: 'Committing hardcoded secrets exposes authentication tokens.',
  suggested_fix: 'Use os.getenv("API_KEY")',
  confidence: 0.95,
};

describe('FindingCard', () => {
  it('displays finding information', () => {
    render(<FindingCard finding={mockFinding} />);

    expect(screen.getByText('Hardcoded Credentials Risk')).toBeInTheDocument();
    expect(screen.getByText('SECURITY')).toBeInTheDocument();
    expect(screen.getByText(/backend\/app\/core\/config.py/)).toBeInTheDocument();
    expect(screen.getByText('Fallback API token detected in configuration settings default value.')).toBeInTheDocument();
  });

  it('expands/collapses contents on click', () => {
    render(<FindingCard finding={mockFinding} />);

    // By default, it is expanded (isExpanded = true). So description/fix is visible.
    const descriptionHeading = screen.getByText('Issue Description');
    expect(descriptionHeading).toBeInTheDocument();

    // Click header to collapse
    const header = screen.getByText('Hardcoded Credentials Risk');
    fireEvent.click(header);

    // It should collapse, so 'Issue Description' should no longer be in the document
    expect(screen.queryByText('Issue Description')).not.toBeInTheDocument();

    // Click again to expand
    fireEvent.click(header);
    expect(screen.getByText('Issue Description')).toBeInTheDocument();
  });
});
