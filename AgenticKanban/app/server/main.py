from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
import sys
from typing import Dict, Any

from core.database import init_db, close_db
from core.api import router as api_router
from core.websocket import websocket_endpoint, global_websocket_endpoint
from core.orchestrator import start_orchestrator, stop_orchestrator


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    await init_db()
    await start_orchestrator()
    yield
    # Shutdown
    await stop_orchestrator()
    await close_db()


app = FastAPI(
    title="AgenticKanban API",
    description="API + WebSocket architecture for Agentic Data Workflows",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React/Vite dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# WebSocket endpoints
app.add_websocket_route("/ws/workflows/{adw_id}", websocket_endpoint)
app.add_websocket_route("/ws/global", global_websocket_endpoint)


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "service": "AgenticKanban API",
        "version": "1.0.0"
    }


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint with API information"""
    return {
        "message": "AgenticKanban API + WebSocket Server",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    # Check for test mode
    test_mode = "--test-mode" in sys.argv

    if test_mode:
        print("Starting API server in test mode...")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if not test_mode else False,
        log_level="info"
    )