from mongoengine import connect, disconnect
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


def connect_to_mongo():
    """Establish connection to MongoDB."""
    try:
        # Add TLS parameters to connection string if not present
        connection_url = settings.MONGODB_URL
        if '?' in connection_url:
            connection_url += '&tls=true&tlsAllowInvalidCertificates=true'
        else:
            connection_url += '?tls=true&tlsAllowInvalidCertificates=true'
        
        connect(
            db=settings.MONGODB_DB_NAME,
            host=connection_url,
            alias='default'
        )
        logger.info(f"Successfully connected to MongoDB: {settings.MONGODB_DB_NAME}")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise


def close_mongo_connection():
    """Close MongoDB connection."""
    try:
        disconnect(alias='default')
        logger.info("MongoDB connection closed")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {str(e)}")
