"""
Strategy Management API Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import date
from uuid import UUID

from app.models.strategy import Strategy, StrategyCreate, StrategyUpdate
from app.services.strategy_service import StrategyService
from app.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/strategies", response_model=Strategy)
async def create_strategy(
    strategy: StrategyCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create a new strategy"""
    service = StrategyService(session)
    created = await service.create_strategy(strategy)
    return created


@router.get("/strategies", response_model=List[Strategy])
async def list_strategies(
    session: AsyncSession = Depends(get_session)
):
    """Get all strategies"""
    service = StrategyService(session)
    strategies = await service.list_strategies()
    return strategies


@router.get("/strategies/{strategy_id}", response_model=Strategy)
async def get_strategy(
    strategy_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    """Get strategy by ID"""
    service = StrategyService(session)
    strategy = await service.get_strategy(strategy_id)
    if strategy is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@router.put("/strategies/{strategy_id}", response_model=Strategy)
async def update_strategy(
    strategy_id: UUID,
    strategy: StrategyUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update strategy"""
    service = StrategyService(session)
    updated = await service.update_strategy(strategy_id, strategy)
    if updated is None:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return updated


@router.delete("/strategies/{strategy_id}")
async def delete_strategy(
    strategy_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    """Delete strategy"""
    service = StrategyService(session)
    success = await service.delete_strategy(strategy_id)
    if not success:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return {"message": "Strategy deleted"}


@router.post("/strategies/preview")
async def preview_strategy(
    strategy: StrategyCreate,
    preview_date: date,
    session: AsyncSession = Depends(get_session)
):
    """Preview strategy stock selection"""
    service = StrategyService(session)
    result = await service.preview_stocks(strategy, preview_date)
    return {"data": result}
