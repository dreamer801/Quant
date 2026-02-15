"""
Backtest Pydantic Models
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from uuid import UUID


class BacktestRequest(BaseModel):
    """Backtest request model"""
    strategy_id: UUID = Field(..., description="Strategy ID")
    start_date: date = Field(..., description="Backtest start date")
    end_date: date = Field(..., description="Backtest end date")
    initial_capital: float = Field(1000000.0, gt=0, description="Initial capital")
    benchmark: Optional[str] = Field("000300.SH", description="Benchmark index code")


class Trade(BaseModel):
    """Single trade record"""
    trade_date: date
    ts_code: str
    direction: str  # "buy" or "sell"
    price: float
    shares: int
    amount: float
    commission: float


class Position(BaseModel):
    """Position at a point in time"""
    ts_code: str
    shares: int
    market_value: float
    weight: float


class NetValuePoint(BaseModel):
    """Net value at a point in time"""
    date: date
    net_value: float
    total_value: float
    cash: float
    positions: List[Position]


class BacktestResult(BaseModel):
    """Backtest result model"""
    id: UUID
    strategy_id: UUID
    start_date: date
    end_date: date
    initial_capital: float
    total_return: Optional[float] = None
    annual_return: Optional[float] = None
    max_drawdown: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    win_rate: Optional[float] = None
    profit_loss_ratio: Optional[float] = None
    excess_return: Optional[float] = None
    net_value_series: Optional[List[Dict[str, Any]]] = None
    trades: Optional[List[Dict[str, Any]]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class BacktestSummary(BaseModel):
    """Summary of backtest performance"""
    total_return: float
    annual_return: float
    max_drawdown: float
    max_drawdown_start: date
    max_drawdown_end: date
    sharpe_ratio: float
    win_rate: float
    profit_loss_ratio: float
    excess_return: float
    total_trades: int
    winning_trades: int
    losing_trades: int
