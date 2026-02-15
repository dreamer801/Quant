"""
Strategy Pydantic Models
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime
from uuid import UUID
from enum import Enum


class Operator(str, Enum):
    """Comparison operators"""
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    EQ = "=="
    NEQ = "!="
    BETWEEN = "between"


class LogicOperator(str, Enum):
    """Logical operators"""
    AND = "and"
    OR = "or"


class RebalanceFrequency(str, Enum):
    """Rebalance frequency"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


class FilterCondition(BaseModel):
    """Filter condition for stock selection"""
    factor_name: str = Field(..., description="Factor name")
    operator: Operator = Field(..., description="Comparison operator")
    value: Union[float, tuple[float, float]] = Field(..., description="Comparison value(s)")
    logic_op: Optional[LogicOperator] = Field(None, description="Logical operator with next condition")


class RankingRule(BaseModel):
    """Ranking rule for stock selection"""
    factor_name: str = Field(..., description="Factor name for ranking")
    ascending: bool = Field(False, description="Sort ascending")
    weight: float = Field(1.0, ge=0, le=1, description="Weight for this factor")


class TradingRule(BaseModel):
    """Trading rules"""
    rebalance_frequency: RebalanceFrequency = Field(RebalanceFrequency.WEEKLY, description="Rebalance frequency")
    max_position_pct: float = Field(0.1, ge=0, le=1, description="Max position percentage per stock")
    cash_reserve_pct: float = Field(0.05, ge=0, le=1, description="Cash reserve percentage")
    commission_rate: float = Field(0.0003, ge=0, description="Commission rate")
    slippage: float = Field(0.0, ge=0, description="Slippage")


class StrategyConfig(BaseModel):
    """Strategy configuration"""
    universe: List[str] = Field(default=["all"], description="Stock universe")
    filter_conditions: List[FilterCondition] = Field(default_factory=list, description="Filter conditions")
    ranking_rules: List[RankingRule] = Field(default_factory=list, description="Ranking rules")
    trading_rule: TradingRule = Field(default_factory=TradingRule, description="Trading rules")
    top_n: int = Field(10, ge=1, le=100, description="Number of stocks to hold")


class StrategyBase(BaseModel):
    """Base strategy model"""
    name: str = Field(..., min_length=1, max_length=100, description="Strategy name")
    description: Optional[str] = Field(None, description="Strategy description")
    config: StrategyConfig = Field(..., description="Strategy configuration")


class StrategyCreate(StrategyBase):
    """Strategy creation model"""
    pass


class StrategyUpdate(BaseModel):
    """Strategy update model"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    config: Optional[StrategyConfig] = None


class Strategy(StrategyBase):
    """Full strategy model with ID and timestamps"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
