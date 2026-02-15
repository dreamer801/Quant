/**
 * Strategy Service - API calls for strategy management
 */
import apiClient from './api';
import { Strategy, StrategyCreate, StrategyUpdate } from '@/types';

export const strategyService = {
  /**
   * Create a new strategy
   */
  async createStrategy(strategy: StrategyCreate): Promise<Strategy> {
    return await apiClient.post('/strategies', strategy);
  },

  /**
   * Get all strategies
   */
  async getStrategies(): Promise<Strategy[]> {
    return await apiClient.get('/strategies');
  },

  /**
   * Get strategy by ID
   */
  async getStrategy(id: string): Promise<Strategy> {
    return await apiClient.get(`/strategies/${id}`);
  },

  /**
   * Update strategy
   */
  async updateStrategy(id: string, strategy: StrategyUpdate): Promise<Strategy> {
    return await apiClient.put(`/strategies/${id}`, strategy);
  },

  /**
   * Delete strategy
   */
  async deleteStrategy(id: string): Promise<{ message: string }> {
    return await apiClient.delete(`/strategies/${id}`);
  },

  /**
   * Preview strategy stock selection
   */
  async previewStrategy(
    strategy: StrategyCreate,
    previewDate: string
  ): Promise<{
    date: string;
    total_count: number;
    filtered_count: number;
    count: number;
    stocks: Record<string, unknown>[];
  }> {
    const response = await apiClient.post('/strategies/preview', strategy, {
      params: { preview_date: previewDate },
    });
    return response;
  },
};

export default strategyService;
