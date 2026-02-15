/**
 * Backtest Types
 */

export interface BacktestRequest {
  strategy_id: string;
  start_date: string;
  end_date: string;
  initial_capital: number;
  benchmark?: string;
}

export interface Trade {
  trade_date: string;
  ts_code: string;
  direction: 'buy' | 'sell';
  price: number;
  shares: number;
  amount: number;
  commission: number;
  pnl?: number;
}

export interface NetValuePoint {
  date: string;
  net_value: number;
  total_value: number;
  cash: number;
}

export interface BacktestResult {
  id: string;
  strategy_id: string;
  start_date: string;
  end_date: string;
  initial_capital: number;
  total_return: number | null;
  annual_return: number | null;
  max_drawdown: number | null;
  sharpe_ratio: number | null;
  win_rate: number | null;
  profit_loss_ratio: number | null;
  excess_return?: number | null;
  net_value_series: NetValuePoint[] | null;
  trades: Trade[] | null;
  created_at: string;
}

export interface BacktestSummary {
  total_return: number;
  annual_return: number;
  max_drawdown: number;
  max_drawdown_start: string;
  max_drawdown_end: string;
  sharpe_ratio: number;
  win_rate: number;
  profit_loss_ratio: number;
  excess_return: number;
  total_trades: number;
  winning_trades: number;
  losing_trades: number;
}
