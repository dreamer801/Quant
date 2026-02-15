# Requirements Document - Quant Investment Platform MVP

## Introduction

本平台是一个"无代码"量化投资平台，类似于"果仁网"。用户无需编写代码，通过简单的 UI 拖拽或条件选择，即可利用历史股票数据进行策略构建和回测。本 MVP 版本为个人使用版本，不包含用户认证系统。

## Glossary

- **Platform**: 量化投资平台系统
- **User**: 平台使用者（单用户）
- **Strategy**: 投资策略，由筛选条件、排名规则和交易规则组成
- **Backtest**: 回测，在历史数据上模拟策略执行并计算收益指标
- **OHLCV**: 开盘价、最高价、最低价、收盘价、成交量
- **Factor**: 因子，用于股票筛选的指标，如市盈率、市值、涨跌幅等
- **Signal**: 交易信号，买入或卖出的触发条件
- **Universe**: 股票池，策略选股的基础范围
- **Tushare/AkShare**: 开源的金融数据接口，提供 A 股历史行情和财务数据

## Requirements

### REQ-001: 数据中心 - 历史行情数据管理

**User Story:** AS 平台使用者，我希望平台提供准确的 A 股历史行情数据，以便进行策略回测分析。

#### Acceptance Criteria

1. WHEN 用户查询指定股票的历史行情，平台 SHALL 返回该股票的 OHLCV 日线数据。
2. WHEN 用户指定时间范围查询，平台 SHALL 返回该时间范围内所有交易日的完整数据。
3. IF 用户查询的股票代码不存在，平台 SHALL 返回明确的错误提示信息。
4. 平台 SHALL 支持至少 5 年的历史数据存储。
5. 平台 SHALL 通过 Tushare 或 AkShare 接口获取 A 股行情数据。

### REQ-002: 数据中心 - 财务数据与基本面因子

**User Story:** AS 平台使用者，我希望平台提供财务数据和基本面因子，以便构建基于基本面的投资策略。

#### Acceptance Criteria

1. WHEN 用户查询股票的财务数据，平台 SHALL 返回该股票的主要财务指标（市盈率、市净率、ROE、营收增长率等）。
2. WHEN 用户查询基本面因子，平台 SHALL 提供不少于 20 个常用因子的历史数据。
3. 平台 SHALL 支持财务数据的季度更新，数据通过 Tushare/AkShare 接口获取。
4. IF 财务数据缺失，平台 SHALL 明确标识缺失的数据字段。

### REQ-003: 数据中心 - 数据缓存与更新

**User Story:** AS 平台使用者，我希望平台能缓存历史数据，以便提高查询和回测效率。

#### Acceptance Criteria

1. WHEN 用户首次查询数据，平台 SHALL 从数据源获取数据并存入本地数据库。
2. WHEN 用户再次查询相同数据，平台 SHALL 优先从本地数据库返回数据。
3. 平台 SHALL 支持手动触发数据更新操作。
4. IF 数据源不可用，平台 SHALL 使用本地缓存数据并提示用户数据可能不是最新。

### REQ-004: 策略构建器 - 筛选条件设置

**User Story:** AS 平台使用者，我希望通过 UI 界面设置股票筛选条件，以便快速构建投资策略。

#### Acceptance Criteria

1. WHEN 用户进入策略构建页面，平台 SHALL 展示可用的筛选因子列表，包括技术指标、财务指标和市场指标。
2. WHEN 用户添加筛选条件，平台 SHALL 提供因子选择、比较运算符（大于、小于、等于、介于）和数值输入的交互界面。
3. WHEN 用户设置多个筛选条件，平台 SHALL 支持条件之间的"与"、"或"逻辑组合。
4. 平台 SHALL 实时展示符合当前筛选条件的股票数量预览。
5. IF 用户设置的筛选条件过于宽松导致匹配股票超过 500 只，平台 SHALL 提示用户增加约束条件。

### REQ-005: 策略构建器 - 排名规则设置

**User Story:** AS 平台使用者，我希望能够设置股票排名规则，以便从筛选结果中选出最优股票组合。

#### Acceptance Criteria

1. WHEN 用户设置排名规则，平台 SHALL 允许用户选择排名依据的因子（如市值、涨跌幅、市盈率等）。
2. WHEN 用户选择排名因子，平台 SHALL 支持设置排序方向（升序或降序）。
3. WHEN 用户设置多个排名因子，平台 SHALL 支持设置因子的权重比例。
4. 平台 SHALL 支持设置选股数量上限（持仓股票数量）。
5. WHEN 用户预览排名结果，平台 SHALL 展示当前排名前 N 的股票列表及其排名依据数值。

### REQ-006: 策略构建器 - 交易规则设置

**User Story:** AS 平台使用者，我希望设置调仓频率和交易规则，以便完整定义策略的执行逻辑。

#### Acceptance Criteria

1. WHEN 用户设置调仓频率，平台 SHALL 提供日频、周频、月频和自定义周期的选项。
2. WHEN 用户设置交易规则，平台 SHALL 允许设置买入信号和卖出信号的条件。
3. 平台 SHALL 支持设置单只股票的最大持仓比例。
4. 平台 SHALL 支持设置现金保留比例。
5. IF 用户未设置交易规则，平台 SHALL 使用默认规则（定期调仓、等权重配置）。

### REQ-007: 回测引擎 - 策略执行与模拟

**User Story:** AS 平台使用者，我希望平台在历史数据上执行我的策略，以便验证策略的有效性。

#### Acceptance Criteria

1. WHEN 用户启动回测任务，平台 SHALL 根据策略定义的时间范围和数据频率执行策略模拟。
2. WHILE 回测执行中，平台 SHALL 按照调仓频率定期触发选股和调仓逻辑。
3. WHEN 执行选股逻辑，平台 SHALL 根据筛选条件和排名规则计算持仓股票列表。
4. 平台 SHALL 记录每次调仓的交易明细（买入/卖出股票、价格、数量、手续费）。
5. IF 回测数据不足，平台 SHALL 中止执行并提示用户调整回测参数。
6. 平台 SHALL 支持设置交易成本（手续费率、滑点），默认费率为 0.0003。

### REQ-008: 回测引擎 - 绩效指标计算

**User Story:** AS 平台使用者，我希望看到策略的详细绩效指标，以便评估策略的投资价值。

#### Acceptance Criteria

1. WHEN 回测完成，平台 SHALL 计算并展示年化收益率。
2. WHEN 回测完成，平台 SHALL 计算并展示最大回撤及其发生时间段。
3. WHEN 回测完成，平台 SHALL 计算并展示夏普比率。
4. WHEN 回测完成，平台 SHALL 计算并展示超额收益（相对基准指数）。
5. WHEN 回测完成，平台 SHALL 计算并展示胜率、盈亏比等交易统计指标。
6. 平台 SHALL 提供策略收益与基准收益的对比数据。

### REQ-009: 可视化大屏 - K线图展示

**User Story:** AS 平台使用者，我希望通过 K 线图直观查看股票走势，以便分析股票的价格变化。

#### Acceptance Criteria

1. WHEN 用户查看股票详情，平台 SHALL 展示该股票的 K 线图。
2. WHEN 用户缩放或平移 K 线图，平台 SHALL 平滑响应并加载对应时间段的数据。
3. 平台 SHALL 在 K 线图上展示成交量柱状图。
4. WHEN 用户选择叠加指标，平台 SHALL 在 K 线图上叠加显示移动平均线、布林带等技术指标。
5. WHEN 用户查看持仓股票，平台 SHALL 在 K 线图上标注买卖信号点。

### REQ-010: 可视化大屏 - 回测结果展示

**User Story:** AS 平台使用者，我希望通过专业图表查看回测结果，以便直观理解策略的表现。

#### Acceptance Criteria

1. WHEN 回测完成，平台 SHALL 展示策略收益曲线图（净值曲线）。
2. WHEN 回测完成，平台 SHALL 展示策略与基准的收益对比图。
3. WHEN 回测完成，平台 SHALL 展示月度收益热力图。
4. WHEN 回测完成，平台 SHALL 展示持仓分布饼图（按行业或市值）。
5. WHEN 用户点击收益曲线上的数据点，平台 SHALL 展示该时间点的持仓详情。
6. 平台 SHALL 支持图表的导出功能（PNG 图片格式）。

### REQ-011: 策略保存与管理

**User Story:** AS 平台使用者，我希望保存和管理我的策略，以便后续修改和复用。

#### Acceptance Criteria

1. WHEN 用户保存策略，平台 SHALL 将策略配置持久化存储，并生成唯一的策略标识。
2. WHEN 用户查看策略列表，平台 SHALL 展示所有创建的策略及其基本信息。
3. WHEN 用户复制策略，平台 SHALL 创建策略副本并允许用户修改。
4. WHEN 用户删除策略，平台 SHALL 在确认后删除策略数据。

---

## Technical Constraints

- **Frontend**: React (Next.js) + TypeScript + Tailwind CSS + ECharts
- **Backend**: Python (FastAPI) - 必须使用 Python 处理金融数据（Pandas/Numpy）
- **Database**: PostgreSQL (TimescaleDB) 或 ClickHouse
- **Data Source**: Tushare 或 AkShare 开源数据接口
- **Backtest Mode**: 同步执行（MVP 阶段）
