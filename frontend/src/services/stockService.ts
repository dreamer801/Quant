/**
 * Stock Service - API calls for stock data
 */
import apiClient from './api';
import { Stock, DailyQuote, FinancialIndicator } from '@/types';

export const stockService = {
  /**
   * Get stock list
   */
  async getStocks(): Promise<Stock[]> {
    const response = await apiClient.get<{ data: Stock[] }>('/stocks');
    return response.data;
  },

  /**
   * Get stock daily quotes
   */
  async getQuotes(
    tsCode: string,
    startDate: string,
    endDate: string
  ): Promise<DailyQuote[]> {
    const response = await apiClient.get<{ data: DailyQuote[] }>(
      `/stocks/${tsCode}/quotes`,
      {
        params: {
          start_date: startDate,
          end_date: endDate,
        },
      }
    );
    return response.data;
  },

  /**
   * Get stock financial indicators
   */
  async getFinancial(tsCode: string): Promise<FinancialIndicator[]> {
    const response = await apiClient.get<{ data: FinancialIndicator[] }>(
      `/stocks/${tsCode}/financial`
    );
    return response.data;
  },

  /**
   * Refresh data from external source
   */
  async refreshData(tsCodes?: string[]): Promise<{ message: string; result: Record<string, unknown> }> {
    const response = await apiClient.post('/data/refresh', { ts_codes: tsCodes });
    return response;
  },
};

export default stockService;
