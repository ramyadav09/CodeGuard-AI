export type Severity = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO';
export type Category = 'BUG' | 'SECURITY' | 'CODE_QUALITY' | 'TESTING' | 'PERFORMANCE' | 'MAINTAINABILITY';

export interface PRMetadata {
  owner: string;
  repo: string;
  pr_number: number;
  title: string;
  author: string;
  html_url: string;
  state: string;
  base_branch: string;
  head_branch: string;
  changed_files_count: number;
  additions: number;
  deletions: number;
}

export interface Finding {
  id?: string;
  severity: Severity;
  category: Category;
  file_path: string;
  line_start?: number | null;
  line_end?: number | null;
  title: string;
  description: string;
  why_it_matters: string;
  suggested_fix: string;
  confidence: number;
}

export interface SeverityBreakdown {
  CRITICAL: number;
  HIGH: number;
  MEDIUM: number;
  LOW: number;
  INFO: number;
}

export interface PRReviewResponse {
  id: string;
  pr_metadata: PRMetadata;
  overall_score: number;
  summary: string;
  findings_count: number;
  severity_breakdown: SeverityBreakdown;
  findings: Finding[];
  created_at: string;
}

export interface PRReviewRequest {
  repo_url?: string;
  owner?: string;
  repo?: string;
  pr_number?: number;
  ai_provider?: string;
}
