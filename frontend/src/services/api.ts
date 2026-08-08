import axios from 'axios';
import type { PRReviewRequest, PRReviewResponse } from '../types/review';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 45000,
});

export const apiService = {
  async getHealth() {
    const res = await client.get('/health');
    return res.data;
  },

  async analyzePR(payload: PRReviewRequest): Promise<PRReviewResponse> {
    const res = await client.post('/review', payload);
    return res.data;
  },

  async getReview(id: string): Promise<PRReviewResponse> {
    const res = await client.get(`/review/${id}`);
    return res.data;
  },

  async getRecentReviews(): Promise<PRReviewResponse[]> {
    const res = await client.get('/recent');
    return res.data;
  },
};
