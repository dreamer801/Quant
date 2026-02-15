"""
Performance Calculator - Calculate backtest performance metrics
"""
import numpy as np
import pandas as pd
from datetime import date
from typing import List, Dict, Any, Tuple, Optional


class PerformanceCalculator:
    """Calculate performance metrics for backtest results"""

    @staticmethod
    def annual_return(returns: pd.Series, periods_per_year: int = 252) -> float:
        """Calculate annualized return"""
        if returns.empty:
            return 0.0

        total_return = (1 + returns).prod() - 1
        n_periods = len(returns)

        if n_periods == 0:
            return 0.0

        annual_return = (1 + total_return) ** (periods_per_year / n_periods) - 1
        return float(annual_return)

    @staticmethod
    def total_return(net_values: pd.Series) -> float:
        """Calculate total return"""
        if net_values.empty or len(net_values) < 2:
            return 0.0

        return float((net_values.iloc[-1] / net_values.iloc[0]) - 1)

    @staticmethod
    def max_drawdown(net_values: pd.Series) -> Tuple[float, Optional[date], Optional[date]]:
        """Calculate maximum drawdown and its period"""
        if net_values.empty or len(net_values) < 2:
            return 0.0, None, None

        # Calculate cumulative maximum
        cummax = net_values.cummax()

        # Calculate drawdown
        drawdown = (net_values - cummax) / cummax

        # Find maximum drawdown
        max_dd = drawdown.min()
        max_dd_end_idx = drawdown.idxmin()

        # Find start of max drawdown period
        max_dd_start_idx = net_values[:max_dd_end_idx].idxmax()

        return float(abs(max_dd)), max_dd_start_idx, max_dd_end_idx

    @staticmethod
    def sharpe_ratio(
        returns: pd.Series,
        risk_free_rate: float = 0.03,
        periods_per_year: int = 252
    ) -> float:
        """Calculate Sharpe ratio"""
        if returns.empty or returns.std() == 0:
            return 0.0

        # Annualize risk-free rate to match return frequency
        rf_per_period = (1 + risk_free_rate) ** (1 / periods_per_year) - 1

        excess_returns = returns - rf_per_period
        sr = excess_returns.mean() / excess_returns.std()

        # Annualize
        return float(sr * np.sqrt(periods_per_year))

    @staticmethod
    def sortino_ratio(
        returns: pd.Series,
        risk_free_rate: float = 0.03,
        periods_per_year: int = 252
    ) -> float:
        """Calculate Sortino ratio (uses downside deviation)"""
        if returns.empty:
            return 0.0

        rf_per_period = (1 + risk_free_rate) ** (1 / periods_per_year) - 1
        excess_returns = returns - rf_per_period

        # Calculate downside deviation
        negative_returns = excess_returns[excess_returns < 0]
        if negative_returns.empty:
            return float('inf')

        downside_std = negative_returns.std()

        if downside_std == 0:
            return 0.0

        sr = excess_returns.mean() / downside_std
        return float(sr * np.sqrt(periods_per_year))

    @staticmethod
    def win_rate(trades: List[Dict[str, Any]]) -> float:
        """Calculate win rate from trade list"""
        if not trades:
            return 0.0

        # Group trades by stock to calculate PnL
        winning = 0
        total = 0

        for trade in trades:
            if trade.get("direction") == "sell":
                total += 1
                if trade.get("pnl", 0) > 0:
                    winning += 1

        return winning / total if total > 0 else 0.0

    @staticmethod
    def profit_loss_ratio(trades: List[Dict[str, Any]]) -> float:
        """Calculate profit/loss ratio"""
        if not trades:
            return 0.0

        profits = []
        losses = []

        for trade in trades:
            if trade.get("direction") == "sell":
                pnl = trade.get("pnl", 0)
                if pnl > 0:
                    profits.append(pnl)
                elif pnl < 0:
                    losses.append(abs(pnl))

        avg_profit = np.mean(profits) if profits else 0
        avg_loss = np.mean(losses) if losses else 0

        return avg_profit / avg_loss if avg_loss > 0 else 0.0

    @staticmethod
    def excess_return(
        strategy_returns: pd.Series,
        benchmark_returns: pd.Series
    ) -> float:
        """Calculate excess return over benchmark"""
        if strategy_returns.empty or benchmark_returns.empty:
            return 0.0

        strategy_annual = PerformanceCalculator.annual_return(strategy_returns)
        benchmark_annual = PerformanceCalculator.annual_return(benchmark_returns)

        return strategy_annual - benchmark_annual

    @staticmethod
    def information_ratio(
        strategy_returns: pd.Series,
        benchmark_returns: pd.Series,
        periods_per_year: int = 252
    ) -> float:
        """Calculate information ratio"""
        if strategy_returns.empty or benchmark_returns.empty:
            return 0.0

        # Align indices
        aligned_strategy, aligned_benchmark = strategy_returns.align(benchmark_returns, join='inner')

        if aligned_strategy.empty:
            return 0.0

        excess_returns = aligned_strategy - aligned_benchmark

        if excess_returns.std() == 0:
            return 0.0

        ir = excess_returns.mean() / excess_returns.std()
        return float(ir * np.sqrt(periods_per_year))

    @staticmethod
    def calculate_monthly_returns(
        net_values: pd.Series
    ) -> pd.DataFrame:
        """Calculate monthly returns from net value series"""
        if net_values.empty:
            return pd.DataFrame()

        # Ensure datetime index
        if not isinstance(net_values.index, pd.DatetimeIndex):
            net_values.index = pd.to_datetime(net_values.index)

        # Resample to month-end and calculate returns
        monthly_nav = net_values.resample('ME').last()
        monthly_returns = monthly_nav.pct_change()

        # Create year-month matrix
        monthly_returns_df = pd.DataFrame({
            'year': monthly_returns.index.year,
            'month': monthly_returns.index.month,
            'return': monthly_returns.values
        })

        pivot = monthly_returns_df.pivot(index='year', columns='month', values='return')

        return pivot

    @staticmethod
    def calculate_all_metrics(
        net_values: pd.Series,
        trades: List[Dict[str, Any]],
        benchmark_values: Optional[pd.Series] = None,
        risk_free_rate: float = 0.03
    ) -> Dict[str, Any]:
        """Calculate all performance metrics"""
        if net_values.empty:
            return {}

        # Calculate daily returns
        returns = net_values.pct_change().dropna()

        metrics = {
            'total_return': PerformanceCalculator.total_return(net_values),
            'annual_return': PerformanceCalculator.annual_return(returns),
            'max_drawdown': 0.0,
            'max_drawdown_start': None,
            'max_drawdown_end': None,
            'sharpe_ratio': PerformanceCalculator.sharpe_ratio(returns, risk_free_rate),
            'sortino_ratio': PerformanceCalculator.sortino_ratio(returns, risk_free_rate),
            'win_rate': PerformanceCalculator.win_rate(trades),
            'profit_loss_ratio': PerformanceCalculator.profit_loss_ratio(trades),
            'volatility': float(returns.std() * np.sqrt(252)),
        }

        # Max drawdown
        max_dd, dd_start, dd_end = PerformanceCalculator.max_drawdown(net_values)
        metrics['max_drawdown'] = max_dd
        metrics['max_drawdown_start'] = dd_start.isoformat() if dd_start else None
        metrics['max_drawdown_end'] = dd_end.isoformat() if dd_end else None

        # Excess return if benchmark provided
        if benchmark_values is not None and not benchmark_values.empty:
            benchmark_returns = benchmark_values.pct_change().dropna()
            aligned_strategy, aligned_benchmark = returns.align(benchmark_returns, join='inner')

            if not aligned_strategy.empty:
                metrics['excess_return'] = PerformanceCalculator.excess_return(
                    aligned_strategy, aligned_benchmark
                )
                metrics['information_ratio'] = PerformanceCalculator.information_ratio(
                    aligned_strategy, aligned_benchmark
                )

        # Trade statistics
        if trades:
            sell_trades = [t for t in trades if t.get('direction') == 'sell']
            metrics['total_trades'] = len(sell_trades)
            metrics['winning_trades'] = len([t for t in sell_trades if t.get('pnl', 0) > 0])
            metrics['losing_trades'] = len([t for t in sell_trades if t.get('pnl', 0) <= 0])

        return metrics
