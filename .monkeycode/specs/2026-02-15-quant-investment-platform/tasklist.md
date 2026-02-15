# 需求实施计划 - Quant Investment Platform MVP

## Phase 1: 项目基础设施搭建

- [ ] 1. 创建项目目录结构
   - 创建 `backend/` 和 `frontend/` 顶层目录
   - 创建后端目录结构: `backend/app/{api,models,services,db,utils}`
   - 创建前端目录结构: `frontend/src/{app,components,hooks,services,stores,types}`
   - 参考设计文档 Project Structure 章节

- [ ] 2. 初始化后端项目 (Python/FastAPI)
   - 创建 `backend/pyproject.toml` 或 `requirements.txt`，声明依赖: fastapi, uvicorn, sqlalchemy, pandas, numpy, tushare, akshare, pydantic
   - 创建 `backend/app/main.py` FastAPI 应用入口
   - 配置 CORS 中间件支持前端跨域访问
   - 参考设计文档 Technology Stack 章节

- [ ] 3. 初始化前端项目 (Next.js)
   - 使用 `npx create-next-app@latest` 初始化 TypeScript 项目
   - 安装依赖: echarts, echarts-for-react, tailwindcss, axios
   - 配置 Tailwind CSS
   - 配置 API 代理 (vite.config.ts 或 next.config.js)
   - 参考设计文档 Technology Stack 章节和 Frontend Reverse Proxy Rule

- [ ] 4. 配置数据库连接
   - 创建 `backend/app/db/database.py`，配置 SQLAlchemy 异步引擎
   - 创建 `backend/app/db/models.py`，定义 ORM 模型
   - 配置数据库连接字符串 (支持 PostgreSQL/TimescaleDB)
   - 参考设计文档 Database Schema 章节

## Phase 2: 数据中心模块 (REQ-001, REQ-002, REQ-003)

- [ ] 5. 实现数据模型 - 股票与行情
   - 在 `backend/app/db/models.py` 中创建 Stock 模型 (ts_code, symbol, name, industry, market, list_date)
   - 创建 DailyQuote 模型 (ts_code, trade_date, open, high, low, close, volume, amount, turnover_rate)
   - 创建 FinancialIndicator 模型 (ts_code, end_date, pe_ratio, pb_ratio, roe, debt_ratio, revenue_growth, profit_growth, total_mv, circ_mv)
   - 参考设计文档 Database Schema 章节和 REQ-001

- [ ] 6. 实现 DataFetcher 抽象接口
   - 创建 `backend/app/services/data_fetcher.py`
   - 定义 DataFetcher 抽象基类 (fetch_daily_quotes, fetch_financial_indicators, fetch_stock_list)
   - 参考设计文档 1.1 DataFetcher Interface

- [ ] 7. 实现 AkShare 数据源适配器
   - 创建 `AkShareFetcher` 类继承 DataFetcher
   - 实现 `fetch_daily_quotes` 方法获取日线行情
   - 实现 `fetch_financial_indicators` 方法获取财务指标
   - 实现 `fetch_stock_list` 方法获取 A 股股票列表
   - 参考设计文档 1.1 DataFetcher Interface 和 REQ-001.5

- [ ] 8. 实现 DataCache 缓存服务
   - 创建 `backend/app/services/data_cache.py`
   - 实现 `get_cached_quotes` 从数据库获取缓存数据
   - 实现 `cache_quotes` 将数据写入数据库
   - 实现 `invalidate_cache` 清除指定股票缓存
   - 参考设计文档 1.2 DataCache Interface 和 REQ-003

- [ ] 9. 实现 DataCenterService 统一数据入口
   - 创建 `backend/app/services/data_center.py`
   - 实现 `get_daily_quotes` 方法 (优先缓存，缓存未命中时从数据源获取)
   - 实现 `get_financial_data` 方法
   - 实现 `get_factor_data` 方法获取因子数据
   - 实现 `refresh_data` 方法手动刷新数据
   - 参考设计文档 1.3 Data Center Service 和 REQ-001, REQ-002, REQ-003

- [ ] 10. 实现数据中心 API 路由
   - 创建 `backend/app/api/data_routes.py`
   - 实现 `GET /api/stocks` 获取股票列表
   - 实现 `GET /api/stocks/{ts_code}/quotes` 获取股票行情
   - 实现 `GET /api/stocks/{ts_code}/financial` 获取财务数据
   - 实现 `POST /api/data/refresh` 刷新数据
   - 参考设计文档 4.1 RESTful API Endpoints 和 REQ-001, REQ-002

- [ ] 11. 检查点 - 数据中心功能验证
   - 确保所有 API 端点可正常访问
   - 验证数据能从 AkShare 获取并存储到数据库
   - 验证缓存逻辑正常工作
   - 如有疑问请询问用户

## Phase 3: 策略引擎模块 (REQ-004, REQ-005, REQ-006, REQ-011)

- [ ] 12. 实现策略数据模型 (Pydantic)
   - 创建 `backend/app/models/strategy.py`
   - 定义 Operator 枚举 (GT, GTE, LT, LTE, EQ, NEQ, BETWEEN)
   - 定义 LogicOperator 枚举 (AND, OR)
   - 定义 FilterCondition 模型 (factor_name, operator, value, logic_op)
   - 定义 RankingRule 模型 (factor_name, ascending, weight)
   - 定义 TradingRule 模型 (rebalance_frequency, max_position_pct, cash_reserve_pct, commission_rate, slippage)
   - 定义 Strategy 模型整合以上组件
   - 参考设计文档 2.1 Strategy Model 和 REQ-004, REQ-005, REQ-006

- [ ] 13. 实现策略数据库模型 (ORM)
   - 在 `backend/app/db/models.py` 中创建 Strategy 表模型
   - 创建 BacktestResult 表模型用于存储回测结果
   - 参考设计文档 Database Schema 章节和 REQ-011

- [ ] 14. 实现因子定义配置
   - 创建 `backend/app/utils/factors.py` 定义因子元数据
   - 定义因子列表 (pe_ratio, pb_ratio, total_mv, circ_mv, turnover_rate, roe, debt_ratio, revenue_growth, profit_growth, return_20d, return_60d, ma_5, ma_20, rsi_14, macd)
   - 每个因子包含: name, display_name, category, description
   - 参考设计文档 Factor Definitions 章节

- [ ] 15. 实现 StrategyService 策略服务
   - 创建 `backend/app/services/strategy_service.py`
   - 实现 `create_strategy` 创建策略并持久化
   - 实现 `get_strategy` 获取单个策略
   - 实现 `list_strategies` 列出所有策略
   - 实现 `update_strategy` 更新策略
   - 实现 `delete_strategy` 删除策略
   - 实现 `validate_strategy` 验证策略配置完整性
   - 参考设计文档 2.2 Strategy Service 和 REQ-011

- [ ] 16. 实现策略选股逻辑
   - 在 StrategyService 中实现 `preview_stocks` 方法
   - 根据筛选条件过滤股票 (支持 AND/OR 逻辑组合)
   - 根据排名规则计算综合得分并排序
   - 返回排名前 N 的股票列表
   - 参考设计文档 2.2 Strategy Service 和 REQ-004, REQ-005

- [ ] 17. 实现策略管理 API 路由
   - 创建 `backend/app/api/strategy_routes.py`
   - 实现 `POST /api/strategies` 创建策略
   - 实现 `GET /api/strategies` 获取策略列表
   - 实现 `GET /api/strategies/{strategy_id}` 获取策略详情
   - 实现 `PUT /api/strategies/{strategy_id}` 更新策略
   - 实现 `DELETE /api/strategies/{strategy_id}` 删除策略
   - 实现 `POST /api/strategies/preview` 预览选股结果
   - 参考设计文档 4.1 RESTful API Endpoints 和 REQ-011

- [ ] 18. 检查点 - 策略引擎功能验证
   - 确保策略 CRUD API 正常工作
   - 验证策略选股预览功能正确
   - 验证筛选条件和排名规则逻辑正确
   - 如有疑问请询问用户

## Phase 4: 回测引擎模块 (REQ-007, REQ-008)

- [ ] 19. 实现绩效计算器
   - 创建 `backend/app/services/performance_calculator.py`
   - 实现 `annual_return` 年化收益率计算
   - 实现 `max_drawdown` 最大回撤计算 (返回回撤值及起止时间)
   - 实现 `sharpe_ratio` 夏普比率计算
   - 实现 `win_rate` 胜率计算
   - 实现 `profit_loss_ratio` 盈亏比计算
   - 实现 `excess_return` 超额收益计算
   - 参考设计文档 3.2 Performance Calculator 和 REQ-008

- [ ] 20. 实现回测引擎核心逻辑
   - 创建 `backend/app/services/backtest_engine.py`
   - 实现 `BacktestEngine` 类初始化 (依赖 DataCenterService, StrategyService)
   - 实现 `_select_stocks` 方法根据策略筛选和排名股票
   - 实现 `_rebalance` 方法执行调仓逻辑
   - 实现交易成本计算 (手续费、滑点)
   - 参考设计文档 3.1 Backtest Engine 和 REQ-007

- [ ] 21. 实现回测主流程
   - 在 BacktestEngine 中实现 `run_backtest` 方法
   - 加载历史数据和交易日历
   - 按调仓频率遍历交易日
   - 在每个调仓日执行选股和调仓
   - 记录每日净值和交易明细
   - 计算并返回绩效指标
   - 参考设计文档 3.1 Backtest Engine 和 REQ-007

- [ ] 22. 实现回测结果模型
   - 创建 `backend/app/models/backtest.py`
   - 定义 BacktestResult 模型 (strategy_id, start_date, end_date, total_return, annual_return, max_drawdown, sharpe_ratio, win_rate, profit_loss_ratio, excess_return, net_value_series, positions_history, trades)
   - 定义 BacktestRequest 模型 (strategy_id, start_date, end_date, initial_capital, benchmark)
   - 参考设计文档 3.1 Backtest Engine 和 REQ-007, REQ-008

- [ ] 23. 实现回测 API 路由
   - 创建 `backend/app/api/backtest_routes.py`
   - 实现 `POST /api/backtest/run` 执行回测
   - 实现 `GET /api/backtest/results/{backtest_id}` 获取回测结果
   - 参考设计文档 4.1 RESTful API Endpoints 和 REQ-007, REQ-008

- [ ] 24. 检查点 - 回测引擎功能验证
   - 创建简单测试策略执行回测
   - 验证绩效指标计算正确
   - 验证交易明细记录完整
   - 如有疑问请询问用户

## Phase 5: 前端基础架构

- [ ] 25. 创建前端类型定义
   - 创建 `frontend/src/types/strategy.ts` 定义 Strategy, FilterCondition, RankingRule, TradingRule 类型
   - 创建 `frontend/src/types/backtest.ts` 定义 BacktestResult, BacktestRequest 类型
   - 创建 `frontend/src/types/stock.ts` 定义 Stock, DailyQuote, FinancialIndicator 类型
   - 参考设计文档 5.1 Strategy Builder Components

- [ ] 26. 实现 API 服务层
   - 创建 `frontend/src/services/api.ts` 封装 axios 实例
   - 创建 `frontend/src/services/stockService.ts` 股票数据相关 API
   - 创建 `frontend/src/services/strategyService.ts` 策略相关 API
   - 创建 `frontend/src/services/backtestService.ts` 回测相关 API
   - 参考设计文档 4.1 RESTful API Endpoints

- [ ] 27. 创建通用组件
   - 创建 `frontend/src/components/common/Layout.tsx` 页面布局组件
   - 创建 `frontend/src/components/common/Header.tsx` 顶部导航组件
   - 创建 `frontend/src/components/common/Sidebar.tsx` 侧边栏组件
   - 创建 `frontend/src/components/common/Button.tsx` 按钮组件
   - 创建 `frontend/src/components/common/Input.tsx` 输入框组件
   - 创建 `frontend/src/components/common/Select.tsx` 下拉选择组件

- [ ] 28. 实现首页和导航
   - 创建 `frontend/src/app/page.tsx` 首页 (展示平台概览)
   - 创建 `frontend/src/app/layout.tsx` 根布局
   - 实现导航菜单 (策略构建、回测、数据管理)

## Phase 6: 策略构建器前端 (REQ-004, REQ-005, REQ-006)

- [ ] 29. 创建策略构建页面框架
   - 创建 `frontend/src/app/strategy/page.tsx` 策略构建主页面
   - 创建 `frontend/src/app/strategy/[id]/page.tsx` 策略编辑页面
   - 设计页面布局 (左侧条件设置，右侧预览)

- [ ] 30. 实现筛选条件组件
   - 创建 `frontend/src/components/StrategyBuilder/FilterConditionBuilder.tsx`
   - 实现因子选择下拉框
   - 实现运算符选择 (大于、小于、等于、介于等)
   - 实现数值输入 (单值或范围值)
   - 实现逻辑运算符选择 (AND/OR)
   - 支持添加/删除多个条件
   - 参考设计文档 5.1 Strategy Builder Components 和 REQ-004

- [ ] 31. 实现排名规则组件
   - 创建 `frontend/src/components/StrategyBuilder/RankingRuleBuilder.tsx`
   - 实现排名因子选择
   - 实现排序方向选择 (升序/降序)
   - 实现权重设置 (多个因子时)
   - 支持添加/删除多个排名规则
   - 参考设计文档 5.1 Strategy Builder Components 和 REQ-005

- [ ] 32. 实现交易规则组件
   - 创建 `frontend/src/components/StrategyBuilder/TradingRuleBuilder.tsx`
   - 实现调仓频率选择 (日频、周频、月频)
   - 实现最大持仓比例设置
   - 实现现金保留比例设置
   - 实现手续费率设置
   - 参考设计文档 5.1 Strategy Builder Components 和 REQ-006

- [ ] 33. 实现策略预览组件
   - 创建 `frontend/src/components/StrategyBuilder/StrategyPreview.tsx`
   - 实时显示符合条件的股票数量
   - 显示当前排名前 N 的股票列表
   - 参考设计文档 REQ-004.4, REQ-005.5

- [ ] 34. 实现策略保存和管理
   - 实现策略保存功能 (调用 POST /api/strategies)
   - 实现策略更新功能 (调用 PUT /api/strategies/{id})
   - 实现策略复制功能
   - 实现策略删除功能 (确认对话框)
   - 参考设计文档 REQ-011

- [ ] 35. 实现策略列表页面
   - 创建 `frontend/src/app/strategies/page.tsx` 策略列表页面
   - 显示所有策略卡片 (名称、描述、创建时间)
   - 支持点击进入编辑或回测

## Phase 7: 可视化大屏 (REQ-009, REQ-010)

- [ ] 36. 实现 K 线图组件
   - 创建 `frontend/src/components/Visualization/KlineChart.tsx`
   - 使用 ECharts 实现 K 线图 (OHLC)
   - 添加成交量柱状图
   - 支持缩放和平移交互
   - 支持叠加移动平均线 (MA5, MA20)
   - 支持标注买卖信号点
   - 参考设计文档 5.2 Visualization Components 和 REQ-009

- [ ] 37. 实现净值曲线图组件
   - 创建 `frontend/src/components/Visualization/EquityCurveChart.tsx`
   - 使用 ECharts 实现净值曲线
   - 同时显示策略净值和基准净值
   - 支持鼠标悬停显示详细数据
   - 参考设计文档 5.2 Visualization Components 和 REQ-010.1, REQ-010.2

- [ ] 38. 实现月度收益热力图组件
   - 创建 `frontend/src/components/Visualization/MonthlyReturnHeatmap.tsx`
   - 使用 ECharts 实现热力图
   - X 轴为月份，Y 轴为年份
   - 颜色深浅表示收益正负和大小
   - 参考设计文档 5.2 Visualization Components 和 REQ-010.3

- [ ] 39. 实现回撤图组件
   - 创建 `frontend/src/components/Visualization/DrawdownChart.tsx`
   - 使用 ECharts 实现回撤曲线
   - 标注最大回撤区间
   - 参考设计文档 5.2 Visualization Components

- [ ] 40. 实现持仓分布饼图组件
   - 创建 `frontend/src/components/Visualization/PositionPieChart.tsx`
   - 使用 ECharts 实现饼图
   - 支持按行业或市值分类显示
   - 参考设计文档 5.2 Visualization Components 和 REQ-010.4

- [ ] 41. 实现交易明细表格组件
   - 创建 `frontend/src/components/Visualization/TradeTable.tsx`
   - 显示交易日期、股票代码、买卖方向、价格、数量、手续费
   - 支持排序和筛选
   - 参考设计文档 5.2 Visualization Components

## Phase 8: 回测结果页面整合 (REQ-007, REQ-008, REQ-010)

- [ ] 42. 创建回测配置页面
   - 创建 `frontend/src/app/backtest/page.tsx` 回测配置页面
   - 选择策略、设置回测时间范围
   - 设置初始资金、基准指数
   - 提交回测请求

- [ ] 43. 创建回测结果展示页面
   - 创建 `frontend/src/app/backtest/results/[id]/page.tsx` 回测结果页面
   - 显示核心绩效指标卡片 (年化收益、最大回撤、夏普比率等)
   - 集成净值曲线图组件
   - 集成月度收益热力图组件
   - 集成回撤图组件
   - 集成持仓分布饼图组件
   - 集成交易明细表格组件
   - 参考设计文档 REQ-010

- [ ] 44. 实现图表导出功能
   - 为 ECharts 图表添加导出 PNG 功能
   - 使用 ECharts toolbox feature
   - 参考设计文档 REQ-010.6

## Phase 9: 集成测试与优化

- [ ] 45. 实现错误处理机制
   - 后端: 创建 `backend/app/api/error_handlers.py` 统一错误处理
   - 定义 ErrorResponse 模型 (code, message, details)
   - 处理 DATA_001, DATA_002, DATA_003, STRAT_001, STRAT_002, BACK_001 错误
   - 前端: 实现全局错误提示组件
   - 参考设计文档 Error Handling 章节

- [ ] 46. 配置前端开发服务器代理
   - 在 vite.config.ts 或 next.config.js 配置 API 代理
   - 将 /api 请求代理到后端服务
   - 参考设计文档和 Frontend Reverse Proxy Rule

- [ ] 47. 创建 Docker 编排文件
   - 创建 `docker-compose.yml`
   - 配置 PostgreSQL 服务
   - 配置后端服务
   - 配置前端服务
   - 配置网络和数据卷

- [ ] 48. 最终检查点 - 完整功能验证
   - 验证数据获取和缓存正常
   - 验证策略创建、保存、编辑功能
   - 验证回测执行和结果展示
   - 验证可视化图表正确渲染
   - 如有疑问请询问用户
