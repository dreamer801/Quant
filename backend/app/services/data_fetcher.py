"""
Data Fetcher - Abstract interface and implementations
"""
from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, List
import pandas as pd


class DataFetcher(ABC):
    """Abstract data fetcher interface"""

    @abstractmethod
    async def fetch_daily_quotes(
        self,
        ts_code: str,
        start_date: date,
        end_date: date
    ) -> pd.DataFrame:
        """Fetch daily OHLCV quotes"""
        pass

    @abstractmethod
    async def fetch_financial_indicators(
        self,
        ts_code: str,
        period: Optional[str] = None
    ) -> pd.DataFrame:
        """Fetch financial indicators"""
        pass

    @abstractmethod
    async def fetch_stock_list(self) -> pd.DataFrame:
        """Fetch stock list"""
        pass

    @abstractmethod
    async def fetch_trading_calendar(
        self,
        start_date: date,
        end_date: date
    ) -> List[date]:
        """Fetch trading calendar"""
        pass


class AkShareFetcher(DataFetcher):
    """AkShare data source implementation"""

    async def fetch_daily_quotes(
        self,
        ts_code: str,
        start_date: date,
        end_date: date
    ) -> pd.DataFrame:
        """Fetch daily quotes from AkShare"""
        import akshare as ak

        # AkShare uses different format: e.g., "000001" for symbol, "sz" or "sh" for market
        symbol = ts_code.split(".")[0]
        market = ts_code.split(".")[1].lower() if "." in ts_code else "sh"

        try:
            # Use stock_zh_a_hist for A-share historical data
            df = ak.stock_zh_a_hist(
                symbol=symbol,
                period="daily",
                start_date=start_date.strftime("%Y%m%d"),
                end_date=end_date.strftime("%Y%m%d"),
                adjust="qfq"  # Forward adjusted price
            )

            if df.empty:
                return pd.DataFrame()

            # Rename columns to match our schema
            df = df.rename(columns={
                "日期": "trade_date",
                "开盘": "open",
                "最高": "high",
                "最低": "low",
                "收盘": "close",
                "成交量": "volume",
                "成交额": "amount",
                "换手率": "turnover_rate",
            })

            df["ts_code"] = ts_code
            df["trade_date"] = pd.to_datetime(df["trade_date"]).dt.date

            # Select and order columns
            columns = ["ts_code", "trade_date", "open", "high", "low", "close", "volume", "amount", "turnover_rate"]
            df = df[[col for col in columns if col in df.columns]]

            return df

        except Exception as e:
            print(f"Error fetching quotes for {ts_code}: {e}")
            return pd.DataFrame()

    async def fetch_financial_indicators(
        self,
        ts_code: str,
        period: Optional[str] = None
    ) -> pd.DataFrame:
        """Fetch financial indicators from AkShare"""
        import akshare as ak

        symbol = ts_code.split(".")[0]

        try:
            # Get financial indicators
            df = ak.stock_financial_analysis_indicator(symbol=symbol)

            if df.empty:
                return pd.DataFrame()

            # Rename columns
            column_mapping = {
                "日期": "end_date",
                "市盈率": "pe_ratio",
                "市净率": "pb_ratio",
                "净资产收益率": "roe",
                "资产负债率": "debt_ratio",
            }

            df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
            df["ts_code"] = ts_code

            if "end_date" in df.columns:
                df["end_date"] = pd.to_datetime(df["end_date"]).dt.date

            return df

        except Exception as e:
            print(f"Error fetching financial indicators for {ts_code}: {e}")
            return pd.DataFrame()

    async def fetch_stock_list(self) -> pd.DataFrame:
        """Fetch A-share stock list from AkShare"""
        import akshare as ak

        try:
            # Get all A-share stocks
            df = ak.stock_zh_a_spot_em()

            # Rename columns
            df = df.rename(columns={
                "代码": "symbol",
                "名称": "name",
            })

            # Create ts_code format
            df["ts_code"] = df["symbol"] + ".SH"
            df.loc[df["symbol"].str.startswith("0"), "ts_code"] = df["symbol"] + ".SZ"
            df.loc[df["symbol"].str.startswith("3"), "ts_code"] = df["symbol"] + ".SZ"

            # Select columns
            columns = ["ts_code", "symbol", "name"]
            df = df[[col for col in columns if col in df.columns]]

            return df

        except Exception as e:
            print(f"Error fetching stock list: {e}")
            return pd.DataFrame()

    async def fetch_trading_calendar(
        self,
        start_date: date,
        end_date: date
    ) -> List[date]:
        """Fetch trading calendar from AkShare"""
        import akshare as ak

        try:
            df = ak.tool_trade_date_hist_sina()
            df["trade_date"] = pd.to_datetime(df["trade_date"]).dt.date

            # Filter by date range
            mask = (df["trade_date"] >= start_date) & (df["trade_date"] <= end_date)
            return df.loc[mask, "trade_date"].tolist()

        except Exception as e:
            print(f"Error fetching trading calendar: {e}")
            # Return weekdays as fallback
            import datetime
            current = start_date
            trading_days = []
            while current <= end_date:
                if current.weekday() < 5:  # Monday to Friday
                    trading_days.append(current)
                current += datetime.timedelta(days=1)
            return trading_days
