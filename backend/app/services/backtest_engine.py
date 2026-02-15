"""
Backtest Engine - Core backtest execution logic
"""
from datetime import date, timedelta
from typing import Optional, List, Dict, Any
from uuid import UUID
import pandas as pd
import numpy as np
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import BacktestResult as BacktestResultModel, Strategy as StrategyModel
from app.models.backtest import BacktestResult
from app.models.strategy import StrategyConfig
from app.services.data_center import DataCenterService
from app.services.strategy_service import StrategyService
from app.services.performance_calculator import PerformanceCalculator


class BacktestEngine:
    """Backtest engine for strategy simulation"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.data_center = DataCenterService(session)
        self.strategy_service = StrategyService(session)

    async def run_backtest(
        self,
        strategy_id: UUID,
        start_date: date,
        end_date: date,
        initial_capital: float = 1000000.0,
        benchmark: Optional[str] = "000300.SH",
    ) -> BacktestResult:
        """Run backtest for a strategy"""
        # Get strategy
        strategy = await self.strategy_service.get_strategy(strategy_id)
        if strategy is None:
            raise ValueError(f"Strategy {strategy_id} not found")

        # Get trading calendar
        trading_days = await self.data_center.get_trading_calendar(start_date, end_date)
        if not trading_days:
            raise ValueError("No trading days in the specified period")

        # Get rebalance dates based on frequency
        config = strategy.config
        rebalance_dates = self._get_rebalance_dates(
            trading_days,
            config.trading_rule.rebalance_frequency
        )

        # Initialize portfolio
        cash = initial_capital * (1 - config.trading_rule.cash_reserve_pct)
        reserved_cash = initial_capital * config.trading_rule.cash_reserve_pct
        positions: Dict[str, Dict[str, Any]] = {}  # ts_code -> {shares, cost}

        # Tracking
        net_values = []
        all_trades = []

        # Run backtest
        for trade_date in trading_days:
            # Update position values
            total_value = cash + reserved_cash

            for ts_code, pos in positions.items():
                # Get today's price
                quotes = await self.data_center.get_daily_quotes(ts_code, trade_date, trade_date)
                if quotes:
                    price = quotes[0].get('close', pos['cost'])
                    total_value += pos['shares'] * price

            # Record net value
            net_values.append({
                'date': trade_date.isoformat(),
                'net_value': total_value / initial_capital,
                'total_value': total_value,
                'cash': cash + reserved_cash,
            })

            # Check if rebalance day
            if trade_date in rebalance_dates:
                # Get stock selection
                selection = await self.strategy_service.preview_stocks(
                    strategy.__class__(**strategy.model_dump()),
                    trade_date
                )

                selected_stocks = [s['ts_code'] for s in selection.get('stocks', [])]

                # Clear existing positions not in selection
                for ts_code in list(positions.keys()):
                    if ts_code not in selected_stocks:
                        # Sell
                        quotes = await self.data_center.get_daily_quotes(ts_code, trade_date, trade_date)
                        if quotes:
                            price = quotes[0].get('close', 0)
                            shares = positions[ts_code]['shares']
                            amount = shares * price
                            commission = amount * config.trading_rule.commission_rate

                            cash += amount - commission

                            all_trades.append({
                                'trade_date': trade_date.isoformat(),
                                'ts_code': ts_code,
                                'direction': 'sell',
                                'price': price,
                                'shares': shares,
                                'amount': amount,
                                'commission': commission,
                            })

                            del positions[ts_code]

                # Buy new positions
                n_stocks = min(config.top_n, len(selected_stocks))
                if n_stocks > 0:
                    position_size = cash * config.trading_rule.max_position_pct

                    for ts_code in selected_stocks[:n_stocks]:
                        if ts_code not in positions:
                            quotes = await self.data_center.get_daily_quotes(ts_code, trade_date, trade_date)
                            if quotes:
                                price = quotes[0].get('close', 0)
                                if price > 0:
                                    shares = int(position_size / price / 100) * 100  # Round to board lot
                                    if shares > 0:
                                        amount = shares * price
                                        commission = amount * config.trading_rule.commission_rate

                                        if amount + commission <= cash:
                                            cash -= amount + commission
                                            positions[ts_code] = {
                                                'shares': shares,
                                                'cost': price,
                                            }

                                            all_trades.append({
                                                'trade_date': trade_date.isoformat(),
                                                'ts_code': ts_code,
                                                'direction': 'buy',
                                                'price': price,
                                                'shares': shares,
                                                'amount': amount,
                                                'commission': commission,
                                            })

        # Calculate performance metrics
        nv_series = pd.Series(
            [v['net_value'] for v in net_values],
            index=pd.to_datetime([v['date'] for v in net_values])
        )

        metrics = PerformanceCalculator.calculate_all_metrics(nv_series, all_trades)

        # Save result to database
        db_result = BacktestResultModel(
            strategy_id=strategy_id,
            start_date=start_date,
            end_date=end_date,
            initial_capital=initial_capital,
            total_return=metrics.get('total_return'),
            annual_return=metrics.get('annual_return'),
            max_drawdown=metrics.get('max_drawdown'),
            sharpe_ratio=metrics.get('sharpe_ratio'),
            win_rate=metrics.get('win_rate'),
            profit_loss_ratio=metrics.get('profit_loss_ratio'),
            net_value_series=net_values,
            trades=all_trades,
        )

        self.session.add(db_result)
        await self.session.commit()
        await self.session.refresh(db_result)

        return BacktestResult(
            id=db_result.id,
            strategy_id=db_result.strategy_id,
            start_date=db_result.start_date,
            end_date=db_result.end_date,
            initial_capital=float(db_result.initial_capital),
            total_return=float(db_result.total_return) if db_result.total_return else None,
            annual_return=float(db_result.annual_return) if db_result.annual_return else None,
            max_drawdown=float(db_result.max_drawdown) if db_result.max_drawdown else None,
            sharpe_ratio=float(db_result.sharpe_ratio) if db_result.sharpe_ratio else None,
            win_rate=float(db_result.win_rate) if db_result.win_rate else None,
            profit_loss_ratio=float(db_result.profit_loss_ratio) if db_result.profit_loss_ratio else None,
            net_value_series=db_result.net_value_series,
            trades=db_result.trades,
            created_at=db_result.created_at,
        )

    async def get_result(self, backtest_id: UUID) -> Optional[BacktestResult]:
        """Get backtest result by ID"""
        result = await self.session.execute(
            select(BacktestResultModel).where(BacktestResultModel.id == backtest_id)
        )
        db_result = result.scalar_one_or_none()

        if db_result is None:
            return None

        return BacktestResult(
            id=db_result.id,
            strategy_id=db_result.strategy_id,
            start_date=db_result.start_date,
            end_date=db_result.end_date,
            initial_capital=float(db_result.initial_capital),
            total_return=float(db_result.total_return) if db_result.total_return else None,
            annual_return=float(db_result.annual_return) if db_result.annual_return else None,
            max_drawdown=float(db_result.max_drawdown) if db_result.max_drawdown else None,
            sharpe_ratio=float(db_result.sharpe_ratio) if db_result.sharpe_ratio else None,
            win_rate=float(db_result.win_rate) if db_result.win_rate else None,
            profit_loss_ratio=float(db_result.profit_loss_ratio) if db_result.profit_loss_ratio else None,
            net_value_series=db_result.net_value_series,
            trades=db_result.trades,
            created_at=db_result.created_at,
        )

    def _get_rebalance_dates(
        self,
        trading_days: List[date],
        frequency: str
    ) -> List[date]:
        """Get rebalance dates based on frequency"""
        if not trading_days:
            return []

        if frequency == "daily":
            return trading_days

        rebalance_dates = []
        last_month = None
        last_week = None

        for d in trading_days:
            if frequency == "weekly":
                week = d.isocalendar()[1]
                year = d.year
                current_week = (year, week)

                if current_week != last_week:
                    rebalance_dates.append(d)
                    last_week = current_week

            elif frequency == "monthly":
                month = (d.year, d.month)

                if month != last_month:
                    rebalance_dates.append(d)
                    last_month = month

        return rebalance_dates
