"""
Strategy Service - Strategy management and stock selection
"""
from datetime import date
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from app.db.models import Strategy as StrategyModel
from app.models.strategy import (
    Strategy,
    StrategyCreate,
    StrategyUpdate,
    StrategyConfig,
    FilterCondition,
    Operator,
    LogicOperator,
)
from app.services.data_center import DataCenterService


class StrategyService:
    """Strategy service"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.data_center = DataCenterService(session)

    async def create_strategy(self, strategy: StrategyCreate) -> Strategy:
        """Create a new strategy"""
        db_strategy = StrategyModel(
            name=strategy.name,
            description=strategy.description,
            config=strategy.config.model_dump(),
        )
        self.session.add(db_strategy)
        await self.session.commit()
        await self.session.refresh(db_strategy)

        return Strategy(
            id=db_strategy.id,
            name=db_strategy.name,
            description=db_strategy.description,
            config=StrategyConfig(**db_strategy.config),
            created_at=db_strategy.created_at,
            updated_at=db_strategy.updated_at,
        )

    async def get_strategy(self, strategy_id: UUID) -> Optional[Strategy]:
        """Get strategy by ID"""
        result = await self.session.execute(
            select(StrategyModel).where(StrategyModel.id == strategy_id)
        )
        db_strategy = result.scalar_one_or_none()

        if db_strategy is None:
            return None

        return Strategy(
            id=db_strategy.id,
            name=db_strategy.name,
            description=db_strategy.description,
            config=StrategyConfig(**db_strategy.config),
            created_at=db_strategy.created_at,
            updated_at=db_strategy.updated_at,
        )

    async def list_strategies(self) -> List[Strategy]:
        """List all strategies"""
        result = await self.session.execute(select(StrategyModel))
        db_strategies = result.scalars().all()

        return [
            Strategy(
                id=s.id,
                name=s.name,
                description=s.description,
                config=StrategyConfig(**s.config),
                created_at=s.created_at,
                updated_at=s.updated_at,
            )
            for s in db_strategies
        ]

    async def update_strategy(self, strategy_id: UUID, strategy: StrategyUpdate) -> Optional[Strategy]:
        """Update strategy"""
        result = await self.session.execute(
            select(StrategyModel).where(StrategyModel.id == strategy_id)
        )
        db_strategy = result.scalar_one_or_none()

        if db_strategy is None:
            return None

        if strategy.name is not None:
            db_strategy.name = strategy.name
        if strategy.description is not None:
            db_strategy.description = strategy.description
        if strategy.config is not None:
            db_strategy.config = strategy.config.model_dump()

        await self.session.commit()
        await self.session.refresh(db_strategy)

        return Strategy(
            id=db_strategy.id,
            name=db_strategy.name,
            description=db_strategy.description,
            config=StrategyConfig(**db_strategy.config),
            created_at=db_strategy.created_at,
            updated_at=db_strategy.updated_at,
        )

    async def delete_strategy(self, strategy_id: UUID) -> bool:
        """Delete strategy"""
        result = await self.session.execute(
            select(StrategyModel).where(StrategyModel.id == strategy_id)
        )
        db_strategy = result.scalar_one_or_none()

        if db_strategy is None:
            return False

        await self.session.delete(db_strategy)
        await self.session.commit()
        return True

    async def validate_strategy(self, strategy: StrategyCreate) -> List[str]:
        """Validate strategy configuration"""
        errors = []

        if not strategy.name:
            errors.append("Strategy name is required")

        if strategy.config.top_n < 1:
            errors.append("top_n must be at least 1")

        if strategy.config.top_n > 100:
            errors.append("top_n cannot exceed 100")

        # Validate filter conditions
        for i, condition in enumerate(strategy.config.filter_conditions):
            if not condition.factor_name:
                errors.append(f"Filter condition {i}: factor_name is required")

        # Validate ranking rules
        total_weight = sum(r.weight for r in strategy.config.ranking_rules)
        if strategy.config.ranking_rules and abs(total_weight - 1.0) > 0.01:
            errors.append(f"Ranking rule weights should sum to 1.0, got {total_weight}")

        return errors

    async def preview_stocks(
        self,
        strategy: StrategyCreate,
        preview_date: date
    ) -> Dict[str, Any]:
        """Preview strategy stock selection"""
        # Get stock universe
        stocks = await self.data_center.get_stock_list()
        stock_df = pd.DataFrame(stocks)

        if stock_df.empty:
            return {"count": 0, "stocks": []}

        # Apply filter conditions
        filtered_df = self._apply_filters(stock_df, strategy.config.filter_conditions, preview_date)

        # Apply ranking rules
        ranked_df = self._apply_ranking(filtered_df, strategy.config.ranking_rules)

        # Get top N
        top_n = strategy.config.top_n
        result_stocks = ranked_df.head(top_n)

        return {
            "date": preview_date.isoformat(),
            "total_count": len(stock_df),
            "filtered_count": len(filtered_df),
            "count": len(result_stocks),
            "stocks": result_stocks.to_dict(orient="records") if not result_stocks.empty else [],
        }

    def _apply_filters(
        self,
        df: pd.DataFrame,
        conditions: List[FilterCondition],
        query_date: date
    ) -> pd.DataFrame:
        """Apply filter conditions to dataframe"""
        if not conditions:
            return df

        result = df.copy()
        mask = pd.Series([True] * len(result), index=result.index)

        for i, condition in enumerate(conditions):
            # Get factor values (placeholder - would need to fetch actual data)
            # For now, just apply basic filtering
            factor_col = condition.factor_name

            if factor_col not in result.columns:
                continue

            if condition.operator == Operator.GT:
                cond_mask = result[factor_col] > condition.value
            elif condition.operator == Operator.GTE:
                cond_mask = result[factor_col] >= condition.value
            elif condition.operator == Operator.LT:
                cond_mask = result[factor_col] < condition.value
            elif condition.operator == Operator.LTE:
                cond_mask = result[factor_col] <= condition.value
            elif condition.operator == Operator.EQ:
                cond_mask = result[factor_col] == condition.value
            elif condition.operator == Operator.NEQ:
                cond_mask = result[factor_col] != condition.value
            elif condition.operator == Operator.BETWEEN:
                if isinstance(condition.value, (list, tuple)) and len(condition.value) == 2:
                    cond_mask = (result[factor_col] >= condition.value[0]) & (result[factor_col] <= condition.value[1])
                else:
                    cond_mask = pd.Series([True] * len(result), index=result.index)
            else:
                cond_mask = pd.Series([True] * len(result), index=result.index)

            # Apply logic operator
            if i > 0 and conditions[i - 1].logic_op == LogicOperator.OR:
                mask = mask | cond_mask
            else:
                mask = mask & cond_mask

        return result[mask]

    def _apply_ranking(
        self,
        df: pd.DataFrame,
        rules: List[Any]
    ) -> pd.DataFrame:
        """Apply ranking rules to dataframe"""
        if df.empty or not rules:
            return df

        result = df.copy()

        # Calculate composite score
        result["_score"] = 0.0

        for rule in rules:
            factor_col = rule.factor_name
            if factor_col not in result.columns:
                continue

            # Normalize factor values
            factor_values = result[factor_col].astype(float)
            min_val = factor_values.min()
            max_val = factor_values.max()

            if max_val - min_val > 0:
                normalized = (factor_values - min_val) / (max_val - min_val)
            else:
                normalized = pd.Series([0.5] * len(result), index=result.index)

            # Reverse for ascending order
            if rule.ascending:
                normalized = 1 - normalized

            result["_score"] += normalized * rule.weight

        # Sort by score descending
        result = result.sort_values("_score", ascending=False)
        result = result.drop(columns=["_score"])

        return result
