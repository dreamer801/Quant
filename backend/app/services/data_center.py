"""
Data Center Service - Unified data access layer
"""
from datetime import date
from typing import Optional, List, Dict, Any
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from app.db.models import Stock, DailyQuote, FinancialIndicator
from app.services.data_fetcher import DataFetcher, AkShareFetcher


class DataCenterService:
    """Data center service - unified data access"""

    def __init__(self, session: AsyncSession, fetcher: Optional[DataFetcher] = None):
        self.session = session
        self.fetcher = fetcher or AkShareFetcher()

    async def get_stock_list(self) -> List[Dict[str, Any]]:
        """Get all stocks from database, fetch from source if empty"""
        # Try to get from database first
        result = await self.session.execute(select(Stock))
        stocks = result.scalars().all()

        if len(stocks) == 0:
            # Fetch from external source
            df = await self.fetcher.fetch_stock_list()
            if not df.empty:
                # Save to database
                for _, row in df.iterrows():
                    stock = Stock(
                        ts_code=row.get("ts_code"),
                        symbol=row.get("symbol"),
                        name=row.get("name"),
                    )
                    self.session.add(stock)
                await self.session.commit()

                # Fetch again
                result = await self.session.execute(select(Stock))
                stocks = result.scalars().all()

        return [
            {
                "ts_code": s.ts_code,
                "symbol": s.symbol,
                "name": s.name,
                "industry": s.industry,
                "market": s.market,
            }
            for s in stocks
        ]

    async def get_daily_quotes(
        self,
        ts_code: str,
        start_date: date,
        end_date: date,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """Get daily quotes - prefer cache"""

        if use_cache:
            # Try database first
            result = await self.session.execute(
                select(DailyQuote)
                .where(
                    and_(
                        DailyQuote.ts_code == ts_code,
                        DailyQuote.trade_date >= start_date,
                        DailyQuote.trade_date <= end_date,
                    )
                )
                .order_by(DailyQuote.trade_date)
            )
            quotes = result.scalars().all()

            if len(quotes) > 0:
                return [
                    {
                        "ts_code": q.ts_code,
                        "trade_date": q.trade_date.isoformat(),
                        "open": float(q.open) if q.open else None,
                        "high": float(q.high) if q.high else None,
                        "low": float(q.low) if q.low else None,
                        "close": float(q.close) if q.close else None,
                        "volume": q.volume,
                        "amount": float(q.amount) if q.amount else None,
                        "turnover_rate": float(q.turnover_rate) if q.turnover_rate else None,
                    }
                    for q in quotes
                ]

        # Fetch from external source
        df = await self.fetcher.fetch_daily_quotes(ts_code, start_date, end_date)

        if df.empty:
            return []

        # Save to database
        for _, row in df.iterrows():
            quote = DailyQuote(
                ts_code=row.get("ts_code"),
                trade_date=row.get("trade_date"),
                open=row.get("open"),
                high=row.get("high"),
                low=row.get("low"),
                close=row.get("close"),
                volume=row.get("volume"),
                amount=row.get("amount"),
                turnover_rate=row.get("turnover_rate"),
            )
            self.session.add(quote)

        await self.session.commit()

        return df.to_dict(orient="records")

    async def get_financial_data(
        self,
        ts_code: str
    ) -> List[Dict[str, Any]]:
        """Get financial indicators"""

        # Try database first
        result = await self.session.execute(
            select(FinancialIndicator)
            .where(FinancialIndicator.ts_code == ts_code)
            .order_by(FinancialIndicator.end_date.desc())
        )
        indicators = result.scalars().all()

        if len(indicators) > 0:
            return [
                {
                    "ts_code": i.ts_code,
                    "end_date": i.end_date.isoformat(),
                    "pe_ratio": float(i.pe_ratio) if i.pe_ratio else None,
                    "pb_ratio": float(i.pb_ratio) if i.pb_ratio else None,
                    "roe": float(i.roe) if i.roe else None,
                    "debt_ratio": float(i.debt_ratio) if i.debt_ratio else None,
                    "revenue_growth": float(i.revenue_growth) if i.revenue_growth else None,
                    "profit_growth": float(i.profit_growth) if i.profit_growth else None,
                    "total_mv": float(i.total_mv) if i.total_mv else None,
                    "circ_mv": float(i.circ_mv) if i.circ_mv else None,
                }
                for i in indicators
            ]

        # Fetch from external source
        df = await self.fetcher.fetch_financial_indicators(ts_code)

        if df.empty:
            return []

        # Save to database
        for _, row in df.iterrows():
            indicator = FinancialIndicator(
                ts_code=row.get("ts_code"),
                end_date=row.get("end_date"),
                pe_ratio=row.get("pe_ratio"),
                pb_ratio=row.get("pb_ratio"),
                roe=row.get("roe"),
                debt_ratio=row.get("debt_ratio"),
            )
            self.session.add(indicator)

        await self.session.commit()

        return df.to_dict(orient="records")

    async def get_factor_data(
        self,
        factor_names: List[str],
        query_date: date,
        universe: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """Get factor data for stock screening"""
        # This would combine data from multiple sources
        # For now, return empty dataframe
        # TODO: Implement full factor data retrieval
        return pd.DataFrame()

    async def refresh_data(
        self,
        ts_codes: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Refresh data from external source"""
        results = {"stocks": 0, "quotes": 0, "errors": []}

        try:
            # Refresh stock list
            df = await self.fetcher.fetch_stock_list()
            if not df.empty:
                for _, row in df.iterrows():
                    existing = await self.session.get(Stock, row.get("ts_code"))
                    if not existing:
                        stock = Stock(
                            ts_code=row.get("ts_code"),
                            symbol=row.get("symbol"),
                            name=row.get("name"),
                        )
                        self.session.add(stock)
                        results["stocks"] += 1
                await self.session.commit()

        except Exception as e:
            results["errors"].append(f"Error refreshing stock list: {str(e)}")

        return results

    async def get_trading_calendar(
        self,
        start_date: date,
        end_date: date
    ) -> List[date]:
        """Get trading calendar"""
        return await self.fetcher.fetch_trading_calendar(start_date, end_date)
