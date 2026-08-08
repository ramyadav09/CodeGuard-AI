import { test, expect } from '@playwright/test';

test.describe('CodeGuard AI PR Review End-to-End Workflow', () => {
  test.beforeEach(async ({ page }) => {
    // Mock backend health endpoint
    await page.route('**/api/v1/health', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'healthy',
          service: 'CodeGuard AI',
          version: '1.0.0',
          environment: 'test',
          ai_provider: 'mock',
        }),
      });
    });

    // Mock backend review analysis endpoint
    await page.route('**/api/v1/review', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          id: 'mock-report-123',
          pr_metadata: {
            owner: 'octocat',
            repo: 'Hello-World',
            pr_number: 1,
            title: 'Fix critical security leak in authentication logic',
            author: 'octocat',
            html_url: 'https://github.com/octocat/Hello-World/pull/1',
            state: 'open',
            base_branch: 'master',
            head_branch: 'patch-1',
            changed_files_count: 2,
            additions: 15,
            deletions: 4,
          },
          overall_score: 55,
          summary: 'CRITICAL RISK: Hardcoded secret detected in configuration defaults.',
          findings_count: 2,
          severity_breakdown: {
            CRITICAL: 1,
            HIGH: 1,
            MEDIUM: 0,
            LOW: 0,
            INFO: 0,
          },
          findings: [
            {
              id: 'f-1',
              severity: 'CRITICAL',
              category: 'SECURITY',
              file_path: 'backend/app/core/config.py',
              line_start: 14,
              line_end: 18,
              title: 'Hardcoded Credentials Risk',
              description: 'Fallback API token detected in configuration settings string default value.',
              why_it_matters: 'Committing hardcoded secrets exposes authentication tokens to public git history.',
              suggested_fix: 'Use os.getenv("API_KEY") without fallback plaintext defaults.',
              confidence: 0.95,
            },
            {
              id: 'f-2',
              severity: 'HIGH',
              category: 'BUG',
              file_path: 'backend/app/services/diff_parser.py',
              line_start: 52,
              line_end: 56,
              title: 'Potential NoneType Dereference',
              description: 'Attempting to access .group(1) on regex search without checking if match is None.',
              why_it_matters: 'Unmatched header formats cause AttributeError at runtime.',
              suggested_fix: 'Add explicit if match: check before accessing regex group parameters.',
              confidence: 0.89,
            },
          ],
          created_at: new Date().toISOString(),
        }),
      });
    });

    // Mock recent reviews endpoint
    await page.route('**/api/v1/recent', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([]),
      });
    });
  });

  test('1. Open Application Dashboard and verify branding', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('text=CodeGuard AI')).toBeVisible();
    await expect(page.locator('text=Analyze Pull Request')).toBeVisible();
  });

  test('2. Select sample PR and submit review pipeline', async ({ page }) => {
    await page.goto('/');
    
    // Click sample PR button
    await page.click('button:has-text("octocat/Hello-World #1")');

    // Verify input populated
    const input = page.locator('input[placeholder*="Paste GitHub PR URL"]');
    await expect(input).toHaveValue('https://github.com/octocat/Hello-World/pull/1');

    // Click Start AI Review
    await page.click('button:has-text("Start AI Review")');

    // Verify Metrics Overview rendering
    await expect(page.locator('text=Fix critical security leak')).toBeVisible();
    await expect(page.locator('text=Overall PR Health')).toBeVisible();
    await expect(page.locator('text=55')).toBeVisible();
  });

  test('3. Filter findings by severity and category', async ({ page }) => {
    await page.goto('/');
    await page.click('button:has-text("octocat/Hello-World #1")');
    await page.click('button:has-text("Start AI Review")');

    // Verify finding cards present
    await expect(page.locator('text=Hardcoded Credentials Risk')).toBeVisible();
    await expect(page.locator('text=Potential NoneType Dereference')).toBeVisible();

    // Click SECURITY category filter
    await page.click('button:has-text("SECURITY")');

    // Verify only security finding visible
    await expect(page.locator('text=Hardcoded Credentials Risk')).toBeVisible();
    await expect(page.locator('text=Potential NoneType Dereference')).not.toBeVisible();
  });

  test('4. Inspect finding details and copy code fix', async ({ page }) => {
    await page.goto('/');
    await page.click('button:has-text("octocat/Hello-World #1")');
    await page.click('button:has-text("Start AI Review")');

    // Inspect finding card contents
    await expect(page.locator('text=Why It Matters')).toBeVisible();
    await expect(page.locator('text=Suggested Fix')).toBeVisible();

    // Verify copy button exists
    const copyButton = page.locator('button:has-text("Copy Fix")').first();
    await expect(copyButton).toBeVisible();
  });
});
