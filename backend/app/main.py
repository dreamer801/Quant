"""
Quant Investment Platform - Main Application Entry
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import init_db
from app.api import data_routes, strategy_routes, backtest_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="Quant Investment Platform API",
    description="无代码量化投资平台后端 API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(data_routes.router, prefix="/api", tags=["Data Center"])
app.include_router(strategy_routes.router, prefix="/api", tags=["Strategy"])
app.include_router(backtest_routes.router, prefix="/api", tags=["Backtest"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Quant Investment Platform API", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
