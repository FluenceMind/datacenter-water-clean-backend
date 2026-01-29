from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.db.mongo import connect_to_mongo, close_mongo_connection
from app.api.health import router as health_router
from app.api.analysis import router as analysis_router
from app.api.history import router as history_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    logger.info("Starting application...")
    connect_to_mongo()
    yield
    # Shutdown
    logger.info("Shutting down application...")
    close_mongo_connection()


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(analysis_router)
app.include_router(history_router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "DataCenter Water Clean API",
        "version": settings.API_VERSION,
        "docs": "/docs"
    }