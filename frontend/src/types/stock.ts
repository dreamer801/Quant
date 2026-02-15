/**
 * Stock Types
 */

export interface Stock {
  ts_code: string;
  symbol: string;
  name: string;
  industry?: string;
  market?: string;
}

export interface DailyQuote {
  ts_code: string;
  trade_date: string;
  open: number | null;
  high: number | null;
  low: number | null;
  close: number | null;
  volume: number | null;
  amount: number | null;
  turnover_rate: number | null;
}

export interface FinancialIndicator {
  ts_code: string;
  end_date: string;
  pe_ratio: number | null;
  pb_ratio: number | null;
  roe: number | null;
  debt_ratio: number | null;
  revenue_growth: number | null;
  profit_growth: number | null;
  total_mv: number | null;
  circ_mv: number | null;
}
