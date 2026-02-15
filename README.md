# Quant Investment Platform

无代码量化投资平台 - 类似果仁网的策略构建与回测系统。

## 功能特性

- **数据中心**: A股历史行情数据、财务数据、基本面因子
- **策略构建器**: 无代码可视化策略构建界面
- **回测引擎**: 历史数据回测与绩效分析
- **可视化大屏**: K线图、净值曲线、收益热力图等

## 技术栈

### 后端
- Python 3.11+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL / TimescaleDB
- Pandas / NumPy
- AkShare (数据源)

### 前端
- Next.js 14
- TypeScript
- Tailwind CSS
- ECharts

## 快速开始

### 使用 Docker Compose

```bash
docker-compose up -d
```

### 本地开发

#### 后端

```bash
cd backend
pip install -e .
uvicorn app.main:app --reload
```

#### 前端

```bash
cd frontend
npm install
npm run dev
```

更多 Windows/WSL 本地运行细节以及自动化脚本说明，参看 `docs/local-dev.md` 与 `scripts/dev.ps1`。

## 项目结构

```
.
├── backend/
│   ├── app/
│   │   ├── api/           # API 路由
│   │   ├── models/        # Pydantic 模型
│   │   ├── services/      # 业务服务
│   │   ├── db/            # 数据库模型
│   │   ├── utils/         # 工具函数
│   │   └── main.py        # 应用入口
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── app/           # 页面路由
│   │   ├── components/    # React 组件
│   │   ├── services/      # API 服务
│   │   └── types/         # TypeScript 类型
│   └── package.json
│
└── docker-compose.yml
```

## API 文档

启动后端服务后，访问以下地址查看 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

MIT
