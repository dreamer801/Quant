"""
Backtest API Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from uuid import UUID

from app.models.backtest import BacktestRequest, BacktestResult
from app.services.backtest_engine import BacktestEngine
from app.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/backtest/run", response_model=BacktestResult)
async def run_backtest(
    request: BacktestRequest,
    session: AsyncSession = Depends(get_session)
):
    """Run backtest for a strategy"""
    engine = BacktestEngine(session)
    try:
        result = await engine.run_backtest(
            strategy_id=request.strategy_id,
            start_date=request.start_date,
            end_date=request.end_date,
            initial_capital=request.initial_capital,
            benchmark=request.benchmark,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/backtest/results/{backtest_id}", response_model=BacktestResult)
async def get_backtest_result(
    backtest_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    """Get backtest result by ID"""
    engine = BacktestEngine(session)
    result = await engine.get_result(backtest_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Backtest result not found")
    return result
