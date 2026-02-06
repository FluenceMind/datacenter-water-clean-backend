import pytest
from unittest.mock import patch, MagicMock
from app.db.mongo import connect_to_mongo, close_mongo_connection


@patch('app.db.mongo.connect')
@patch('app.db.mongo.settings')
def test_connect_to_mongo_success(mock_settings, mock_connect):
    """Test successful MongoDB connection."""
    mock_settings.MONGODB_DB_NAME = "test_db"
    mock_settings.MONGODB_URL = "mongodb://localhost:27017"
    
    connect_to_mongo()
    
    mock_connect.assert_called_once_with(
        db="test_db",
        host="mongodb://localhost:27017",
        alias='default'
    )


@patch('app.db.mongo.connect')
@patch('app.db.mongo.settings')
def test_connect_to_mongo_failure(mock_settings, mock_connect):
    """Test MongoDB connection failure raises exception."""
    mock_settings.MONGODB_DB_NAME = "test_db"
    mock_settings.MONGODB_URL = "mongodb://invalid:27017"
    mock_connect.side_effect = Exception("Connection failed")
    
    with pytest.raises(Exception) as exc_info:
        connect_to_mongo()
    
    assert "Connection failed" in str(exc_info.value)


@patch('app.db.mongo.disconnect')
def test_close_mongo_connection_success(mock_disconnect):
    """Test successful MongoDB disconnection."""
    close_mongo_connection()
    
    mock_disconnect.assert_called_once_with(alias='default')
