# 本地开发指南

本指南面向在 Windows（含 WSL2）环境下本地运行 Quant 项目的开发者，覆盖数据库配置、后端/前端启动以及常见故障排查。

## 依赖要求

- Docker Desktop 4.25+，已启用 WSL2 后端
- Python 3.11（建议安装在 WSL 或虚拟环境中）
- Node.js 18+ 与 npm 9+
- Git

## 环境变量

### 后端 `.env`

默认无需创建 `.env`，`app/core/config.py` 会连接 `postgresql+asyncpg://postgres:postgres@localhost:5432/quant_platform`。若在 Docker Compose 网络中运行，可设置：

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/quant_platform
```

### 前端 `.env.local`

在 `frontend/.env.local` 中设置后端地址，示例：

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 启动步骤

### 1. 启动数据库

```
docker compose up postgres -d
```

容器准备好后，可通过 `docker compose ps postgres` 查看状态。数据库凭据位于 `docker-compose.yml` 的 `POSTGRES_*` 变量中。

### 2. 启动后端

```
cd backend
pip install -e .
uvicorn app.main:app --reload
```

确保 `DATABASE_URL` 指向可访问的 Postgres；策略保存、回测等功能都依赖数据库写入。

### 3. 启动前端

```
cd frontend
npm install
npm run dev
```

前端通过 `NEXT_PUBLIC_API_URL` 或 Next.js `rewrites` 访问后端，默认使用 `http://localhost:8000`。

## 快捷脚本（Windows PowerShell）

执行 `scripts/dev.ps1` 可自动：

1. 运行 `docker compose up -d postgres`
2. 启动后端（开启新 PowerShell 窗口，自动设置 `DATABASE_URL`）
3. 启动前端（可通过 `-SkipFrontend` 仅运行后端）

```
powershell -ExecutionPolicy Bypass -File scripts/dev.ps1
```

脚本会在每次启动前执行 `pip install -e .` 和 `npm install`，避免依赖缺失。

## 常见问题排查

- **策略无法保存**：检查 Postgres 容器是否运行、`DATABASE_URL` 是否指向 `localhost` 或 Compose 服务名 `postgres`。未连接数据库时会在后端日志看到 `Name or service not known`。
- **前端请求 500/404**：确认 `NEXT_PUBLIC_API_URL` 与后端端口一致；若使用 Next.js rewrites，确保后端运行在 8000 端口。
- **数据库迁移失败**：本地调试不建议切换到 SQLite，部分表（如 `strategies.config` JSONB 字段）必须使用 Postgres。

如需更多部署协助，可在提交 PR 前附带日志或运行 `uvicorn` 与 `docker compose` 输出，便于复现问题。
