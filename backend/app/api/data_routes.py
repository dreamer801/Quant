"""
Data Center API Routes
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from datetime import date
from typing import Optional, List

from app.services.data_center import DataCenterService
from app.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/stocks")
async def list_stocks(
    session: AsyncSession = Depends(get_session)
):
    """Get stock list"""
    service = DataCenterService(session)
    stocks = await service.get_stock_list()
    return {"data": stocks}


@router.get("/stocks/{ts_code}/quotes")
async def get_stock_quotes(
    ts_code: str,
    start_date: date = Query(..., description="Start date"),
    end_date: date = Query(..., description="End date"),
    session: AsyncSession = Depends(get_session)
):
    """Get stock daily quotes"""
    service = DataCenterService(session)
    quotes = await service.get_daily_quotes(ts_code, start_date, end_date)
    if quotes is None or len(quotes) == 0:
        raise HTTPException(status_code=404, detail=f"Stock {ts_code} data not found")
    return {"data": quotes}


@router.get("/stocks/{ts_code}/financial")
async def get_stock_financial(
    ts_code: str,
    session: AsyncSession = Depends(get_session)
):
    """Get stock financial indicators"""
    service = DataCenterService(session)
    financial = await service.get_financial_data(ts_code)
    if financial is None or len(financial) == 0:
        raise HTTPException(status_code=404, detail=f"Stock {ts_code} financial data not found")
    return {"data": financial}


@router.post("/data/refresh")
async def refresh_data(
    ts_codes: Optional[List[str]] = None,
    session: AsyncSession = Depends(get_session)
):
    """Refresh data from external source"""
    service = DataCenterService(session)
    result = await service.refresh_data(ts_codes)
    return {"message": "Data refresh completed", "result": result}
