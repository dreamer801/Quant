"""
Database ORM Models
"""
from datetime import date, datetime
from uuid import uuid4
from sqlalchemy import String, Text, Numeric, BigInteger, Date, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Stock(Base):
    """Stock basic information"""
    __tablename__ = "stocks"

    ts_code: Mapped[str] = mapped_column(String(20), primary_key=True, comment="股票代码 TS格式")
    symbol: Mapped[str] = mapped_column(String(10), nullable=False, comment="股票代码")
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="股票名称")
    industry: Mapped[str | None] = mapped_column(String(50), comment="所属行业")
    market: Mapped[str | None] = mapped_column(String(20), comment="市场类型")
    list_date: Mapped[date | None] = mapped_column(Date, comment="上市日期")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    daily_quotes: Mapped[list["DailyQuote"]] = relationship(back_populates="stock", cascade="all, delete-orphan")
    financial_indicators: Mapped[list["FinancialIndicator"]] = relationship(back_populates="stock", cascade="all, delete-orphan")


class DailyQuote(Base):
    """Daily stock quotes (OHLCV)"""
    __tablename__ = "daily_quotes"

    ts_code: Mapped[str] = mapped_column(String(20), ForeignKey("stocks.ts_code"), primary_key=True, comment="股票代码")
    trade_date: Mapped[date] = mapped_column(Date, primary_key=True, comment="交易日期")
    open: Mapped[float | None] = mapped_column(Numeric(10, 2), comment="开盘价")
    high: Mapped[float | None] = mapped_column(Numeric(10, 2), comment="最高价")
    low: Mapped[float | None] = mapped_column(Numeric(10, 2), comment="最低价")
    close: Mapped[float | None] = mapped_column(Numeric(10, 2), comment="收盘价")
    volume: Mapped[int | None] = mapped_column(BigInteger, comment="成交量")
    amount: Mapped[float | None] = mapped_column(Numeric(20, 2), comment="成交额")
    turnover_rate: Mapped[float | None] = mapped_column(Numeric(10, 4), comment="换手率")

    # Relationships
    stock: Mapped["Stock"] = relationship(back_populates="daily_quotes")

    __table_args__ = (
        Index("ix_daily_quotes_trade_date", "trade_date"),
    )


class FinancialIndicator(Base):
    """Financial indicators for stocks"""
    __tablename__ = "financial_indicators"

    ts_code: Mapped[str] = mapped_column(String(20), ForeignKey("stocks.ts_code"), primary_key=True, comment="股票代码")
    end_date: Mapped[date] = mapped_column(Date, primary_key=True, comment="报告期")
    pe_ratio: Mapped[float | None] = mapped_column(Numeric(10, 4), comment="市盈率 PE")
    pb_ratio: Mapped[float | None] = mapped_column(Numeric(10, 4), comment="市净率 PB")
    roe: Mapped[float | None] = mapped_column(Numeric(10, 4), comment="净资产收益率 ROE")
    debt_ratio: Mapped[float | None] = mapped_column(Numeric(10, 4), comment="资产负债率")
    revenue_growth: Mapped[float | None] = mapped_column(Numeric(10, 4), comment="营收增长率")
    profit_growth: Mapped[float | None] = mapped_column(Numeric(10, 4), comment="利润增长率")
    total_mv: Mapped[float | None] = mapped_column(Numeric(20, 2), comment="总市值")
    circ_mv: Mapped[float | None] = mapped_column(Numeric(20, 2), comment="流通市值")

    # Relationships
    stock: Mapped["Stock"] = relationship(back_populates="financial_indicators")


class Strategy(Base):
    """Investment strategy"""
    __tablename__ = "strategies"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="策略名称")
    description: Mapped[str | None] = mapped_column(Text, comment="策略描述")
    config: Mapped[dict] = mapped_column(JSONB, nullable=False, comment="策略配置 JSON")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    backtest_results: Mapped[list["BacktestResult"]] = relationship(back_populates="strategy", cascade="all, delete-orphan")


class BacktestResult(Base):
    """Backtest results"""
    __tablename__ = "backtest_results"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    strategy_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("strategies.id"), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False, comment="回测开始日期")
    end_date: Mapped[date] = mapped_column(Date, nullable=False, comment="回测结束日期")
    initial_capital: Mapped[float] = mapped_column(Numeric(20, 2), comment="初始资金")
    total_return: Mapped[float | None] = mapped_column(Numeric(10, 4), comment="总收益率")
    annual_return: Mapped[float | None] = mapped_column(Numeric(10, 4), comment="年化收益率")
    max_drawdown: Mapped[float | None] = mapped_column(Numeric(10, 4), comment="最大回撤")
    sharpe_ratio: Mapped[float | None] = mapped_column(Numeric(10, 4), comment="夏普比率")
    win_rate: Mapped[float | None] = mapped_column(Numeric(10, 4), comment="胜率")
    profit_loss_ratio: Mapped[float | None] = mapped_column(Numeric(10, 4), comment="盈亏比")
    net_value_series: Mapped[dict | None] = mapped_column(JSONB, comment="净值序列")
    trades: Mapped[dict | None] = mapped_column(JSONB, comment="交易记录")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    strategy: Mapped["Strategy"] = relationship(back_populates="backtest_results")
