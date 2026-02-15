# Quant Platform Backend

FastAPI backend for the Quant Investment Platform.

## 开发环境

```bash
# 安装依赖
pip install -e .

# 运行服务
uvicorn app.main:app --reload
```

默认数据库连接指向 `postgresql+asyncpg://postgres:postgres@localhost:5432/quant_platform`，如在 Docker Compose 中运行，可通过 `DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/quant_platform` 覆盖。
