import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { PRInputForm } from '../PRInputForm';

describe('PRInputForm', () => {
  it('submits a valid PR URL', () => {
    const handleAnalyze = vi.fn();
    render(<PRInputForm onAnalyze={handleAnalyze} isLoading={false} />);

    const input = screen.getByPlaceholderText(/Paste GitHub PR URL/i);
    const button = screen.getByRole('button', { name: /Start AI Review/i });

    fireEvent.change(input, { target: { value: 'https://github.com/owner/repo/pull/123' } });
    fireEvent.click(button);

    expect(handleAnalyze).toHaveBeenCalledWith({
      repo_url: 'https://github.com/owner/repo/pull/123',
      ai_provider: 'gemini',
    });
  });

  it('shows error message on empty submit', () => {
    const handleAnalyze = vi.fn();
    render(<PRInputForm onAnalyze={handleAnalyze} isLoading={false} />);

    const button = screen.getByRole('button', { name: /Start AI Review/i });
    fireEvent.click(button);

    expect(handleAnalyze).not.toHaveBeenCalled();
    expect(screen.getByText(/Please enter a GitHub Pull Request URL/i)).toBeInTheDocument();
  });
});
