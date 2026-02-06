"""
Test analysis API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from io import BytesIO
from datetime import datetime

from app.main import app

client = TestClient(app)


class TestAnalysisEndpoints:
    """Test analysis upload and retrieval endpoints"""
    
    @patch('app.api.analysis.CSVService')
    @patch('app.api.analysis.RecommendationService')
    @patch('app.api.analysis.WaterAnalysis')
    def test_upload_csv_success(self, mock_water_analysis, mock_recommendation, mock_csv_service):
        """Test successful CSV upload and analysis"""
        # Mock CSV service - need to handle async method
        mock_csv_service.validate_and_parse_csv = AsyncMock(return_value=Mock())
        mock_csv_service.calculate_statistics.return_value = {
            'avg_ph': 7.5,
            'ph_category': 'Target',
            'avg_tds': 150,
            'tds_category': 'Moderate',
            'row_count': 10,
            'min_ph': 7.2,
            'max_ph': 7.8,
            'min_tds': 140,
            'max_tds': 160
        }
        
        # Mock recommendation service
        mock_recommendation.get_recommendation.return_value = (
            "No treatment required",
            "Water is clean"
        )
        
        # Mock database save
        mock_analysis_instance = Mock()
        mock_analysis_instance.id = "507f1f77bcf86cd799439011"
        mock_analysis_instance.upload_timestamp = datetime(2026, 2, 5, 12, 0, 0)
        mock_analysis_instance.original_filename = "test.csv"
        mock_analysis_instance.site_name = "Test Site"
        mock_water_analysis.return_value = mock_analysis_instance
        
        # Create test CSV file
        csv_content = b"pH,TDS\n7.5,150\n7.6,155\n7.4,145"
        
        # Make request
        response = client.post(
            "/api/v1/analysis/upload",
            files={"file": ("test.csv", BytesIO(csv_content), "text/csv")},
            data={"site_name": "Test Site"}
        )
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "analysis_id" in data
        assert data["original_filename"] == "test.csv"
        assert data["site_name"] == "Test Site"
        assert "summary" in data
        assert "recommendation" in data
    
    def test_upload_invalid_file_type(self):
        """Test upload with non-CSV file"""
        txt_content = b"This is not a CSV"
        
        response = client.post(
            "/api/v1/analysis/upload",
            files={"file": ("test.txt", BytesIO(txt_content), "text/plain")}
        )
        
        assert response.status_code == 400
        assert "Invalid file type" in response.json()["detail"]
