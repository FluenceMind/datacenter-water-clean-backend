import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


@patch('app.db.mongo.connect')
@patch('app.db.mongo.disconnect')
def test_app_lifespan(mock_disconnect, mock_connect):
    """Test application startup and shutdown."""
    from app.main import app
    
    with TestClient(app):
        # Startup should call connect
        assert mock_connect.called
    
    # Shutdown should call disconnect
    assert mock_disconnect.called


def test_routers_included():
    """Test that all routers are included in the app."""
    from app.main import app
    
    routes = [route.path for route in app.routes]
    
    # Check that main endpoints exist
    assert "/" in routes
    assert "/health" in routes
    assert any("/api/v1/analysis" in route for route in routes)
