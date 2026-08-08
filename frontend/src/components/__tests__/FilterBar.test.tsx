import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { FilterBar } from '../FilterBar';

describe('FilterBar', () => {
  it('triggers severity selection callback', () => {
    const onSelectSeverity = vi.fn();
    const onSelectCategory = vi.fn();
    const onSearchQueryChange = vi.fn();

    render(
      <FilterBar
        selectedSeverity="ALL"
        onSelectSeverity={onSelectSeverity}
        selectedCategory="ALL"
        onSelectCategory={onSelectCategory}
        searchQuery=""
        onSearchQueryChange={onSearchQueryChange}
      />
    );

    const criticalBtn = screen.getByRole('button', { name: 'CRITICAL' });
    fireEvent.click(criticalBtn);

    expect(onSelectSeverity).toHaveBeenCalledWith('CRITICAL');
  });

  it('triggers category selection callback', () => {
    const onSelectSeverity = vi.fn();
    const onSelectCategory = vi.fn();
    const onSearchQueryChange = vi.fn();

    render(
      <FilterBar
        selectedSeverity="ALL"
        onSelectSeverity={onSelectSeverity}
        selectedCategory="ALL"
        onSelectCategory={onSelectCategory}
        searchQuery=""
        onSearchQueryChange={onSearchQueryChange}
      />
    );

    const securityBtn = screen.getByRole('button', { name: 'SECURITY' });
    fireEvent.click(securityBtn);

    expect(onSelectCategory).toHaveBeenCalledWith('SECURITY');
  });
});
