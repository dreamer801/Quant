"""
Factor definitions and metadata
"""
from typing import List, Dict, Any
from enum import Enum


class FactorCategory(str, Enum):
    """Factor categories"""
    VALUATION = "valuation"
    SIZE = "size"
    TECHNICAL = "technical"
    QUALITY = "quality"
    GROWTH = "growth"
    MOMENTUM = "momentum"


class FactorDefinition:
    """Factor definition with metadata"""

    def __init__(
        self,
        name: str,
        display_name: str,
        category: FactorCategory,
        description: str,
        unit: str = "",
        higher_is_better: bool = True,
    ):
        self.name = name
        self.display_name = display_name
        self.category = category
        self.description = description
        self.unit = unit
        self.higher_is_better = higher_is_better

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "display_name": self.display_name,
            "category": self.category.value,
            "description": self.description,
            "unit": self.unit,
            "higher_is_better": self.higher_is_better,
        }


# Predefined factors
FACTOR_DEFINITIONS: List[FactorDefinition] = [
    # Valuation factors
    FactorDefinition(
        name="pe_ratio",
        display_name="市盈率",
        category=FactorCategory.VALUATION,
        description="股价/每股收益，衡量股票估值水平",
        unit="倍",
        higher_is_better=False,
    ),
    FactorDefinition(
        name="pb_ratio",
        display_name="市净率",
        category=FactorCategory.VALUATION,
        description="股价/每股净资产，衡量相对资产价值",
        unit="倍",
        higher_is_better=False,
    ),
    FactorDefinition(
        name="ps_ratio",
        display_name="市销率",
        category=FactorCategory.VALUATION,
        description="市值/营业收入，衡量相对销售价值",
        unit="倍",
        higher_is_better=False,
    ),

    # Size factors
    FactorDefinition(
        name="total_mv",
        display_name="总市值",
        category=FactorCategory.SIZE,
        description="总股本 x 收盘价",
        unit="亿元",
        higher_is_better=False,
    ),
    FactorDefinition(
        name="circ_mv",
        display_name="流通市值",
        category=FactorCategory.SIZE,
        description="流通股本 x 收盘价",
        unit="亿元",
        higher_is_better=False,
    ),

    # Quality factors
    FactorDefinition(
        name="roe",
        display_name="ROE",
        category=FactorCategory.QUALITY,
        description="净资产收益率，衡量盈利能力",
        unit="%",
        higher_is_better=True,
    ),
    FactorDefinition(
        name="roa",
        display_name="ROA",
        category=FactorCategory.QUALITY,
        description="总资产收益率，衡量资产利用效率",
        unit="%",
        higher_is_better=True,
    ),
    FactorDefinition(
        name="debt_ratio",
        display_name="资产负债率",
        category=FactorCategory.QUALITY,
        description="负债/总资产，衡量财务风险",
        unit="%",
        higher_is_better=False,
    ),
    FactorDefinition(
        name="gross_margin",
        display_name="毛利率",
        category=FactorCategory.QUALITY,
        description="(营收-成本)/营收，衡量盈利质量",
        unit="%",
        higher_is_better=True,
    ),
    FactorDefinition(
        name="net_margin",
        display_name="净利率",
        category=FactorCategory.QUALITY,
        description="净利润/营收，衡量盈利能力",
        unit="%",
        higher_is_better=True,
    ),

    # Growth factors
    FactorDefinition(
        name="revenue_growth",
        display_name="营收增长率",
        category=FactorCategory.GROWTH,
        description="同比营收增长率",
        unit="%",
        higher_is_better=True,
    ),
    FactorDefinition(
        name="profit_growth",
        display_name="利润增长率",
        category=FactorCategory.GROWTH,
        description="同比净利润增长率",
        unit="%",
        higher_is_better=True,
    ),
    FactorDefinition(
        name="eps_growth",
        display_name="EPS增长率",
        category=FactorCategory.GROWTH,
        description="每股收益同比增长率",
        unit="%",
        higher_is_better=True,
    ),

    # Technical factors
    FactorDefinition(
        name="turnover_rate",
        display_name="换手率",
        category=FactorCategory.TECHNICAL,
        description="成交量/流通股本，衡量交易活跃度",
        unit="%",
        higher_is_better=False,
    ),
    FactorDefinition(
        name="return_5d",
        display_name="5日涨幅",
        category=FactorCategory.MOMENTUM,
        description="5个交易日涨跌幅",
        unit="%",
        higher_is_better=True,
    ),
    FactorDefinition(
        name="return_20d",
        display_name="20日涨幅",
        category=FactorCategory.MOMENTUM,
        description="20个交易日涨跌幅",
        unit="%",
        higher_is_better=True,
    ),
    FactorDefinition(
        name="return_60d",
        display_name="60日涨幅",
        category=FactorCategory.MOMENTUM,
        description="60个交易日涨跌幅",
        unit="%",
        higher_is_better=True,
    ),
    FactorDefinition(
        name="ma_5",
        display_name="5日均线",
        category=FactorCategory.TECHNICAL,
        description="5日收盘价移动平均",
        unit="元",
        higher_is_better=True,
    ),
    FactorDefinition(
        name="ma_20",
        display_name="20日均线",
        category=FactorCategory.TECHNICAL,
        description="20日收盘价移动平均",
        unit="元",
        higher_is_better=True,
    ),
    FactorDefinition(
        name="rsi_14",
        display_name="RSI(14)",
        category=FactorCategory.TECHNICAL,
        description="14日相对强弱指标",
        unit="",
        higher_is_better=False,
    ),
    FactorDefinition(
        name="macd",
        display_name="MACD",
        category=FactorCategory.TECHNICAL,
        description="异同移动平均线",
        unit="",
        higher_is_better=True,
    ),
]


def get_factor_by_name(name: str) -> Optional[FactorDefinition]:
    """Get factor definition by name"""
    for factor in FACTOR_DEFINITIONS:
        if factor.name == name:
            return factor
    return None


def get_factors_by_category(category: FactorCategory) -> List[FactorDefinition]:
    """Get all factors in a category"""
    return [f for f in FACTOR_DEFINITIONS if f.category == category]


def get_all_factors() -> List[Dict[str, Any]]:
    """Get all factor definitions as list of dicts"""
    return [f.to_dict() for f in FACTOR_DEFINITIONS]
