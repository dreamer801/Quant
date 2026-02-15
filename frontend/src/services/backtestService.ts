/**
 * Backtest Service - API calls for backtest operations
 */
import apiClient from './api';
import { BacktestRequest, BacktestResult } from '@/types';

export const backtestService = {
  /**
   * Run backtest
   */
  async runBacktest(request: BacktestRequest): Promise<BacktestResult> {
    return await apiClient.post('/backtest/run', request);
  },

  /**
   * Get backtest result by ID
   */
  async getResult(id: string): Promise<BacktestResult> {
    return await apiClient.get(`/backtest/results/${id}`);
  },
};

export default backtestService;
