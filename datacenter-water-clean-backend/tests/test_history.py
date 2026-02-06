"""
Test history API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from app.main import app

client = TestClient(app)


class TestHistoryEndpoints:
    """Test history retrieval endpoints"""
    
    @patch('app.api.history.WaterAnalysis')
    def test_get_history_success(self, mock_water_analysis):
        """Test successful retrieval of analysis history"""
        # Mock database query
        mock_objects = Mock()
        mock_objects.count.return_value = 2
        
        # Create mock analysis records
        mock_analysis_1 = Mock()
        mock_analysis_1.id = "507f1f77bcf86cd799439011"
        mock_analysis_1.upload_timestamp = datetime(2026, 2, 5, 12, 0, 0)
        mock_analysis_1.original_filename = "test1.csv"
        mock_analysis_1.site_name = "Site A"
        mock_analysis_1.avg_ph = 7.5
        mock_analysis_1.ph_category = "Target"
        mock_analysis_1.avg_tds = 150
        mock_analysis_1.tds_category = "Moderate"
        mock_analysis_1.treatment_train = "No treatment required"
        mock_analysis_1.explanation = "Water is clean"
        mock_analysis_1.user_notes = "Applied basic filtration"
        
        mock_analysis_2 = Mock()
        mock_analysis_2.id = "507f1f77bcf86cd799439012"
        mock_analysis_2.upload_timestamp = datetime(2026, 2, 4, 10, 0, 0)
        mock_analysis_2.original_filename = "test2.csv"
        mock_analysis_2.site_name = "Site B"
        mock_analysis_2.avg_ph = 8.0
        mock_analysis_2.ph_category = "High"
        mock_analysis_2.avg_tds = 200
        mock_analysis_2.tds_category = "Moderate"
        mock_analysis_2.treatment_train = "H₂SO₄ acid dosing + RO"
        mock_analysis_2.explanation = "High pH requires acid treatment"
        mock_analysis_2.user_notes = None
        
        mock_skip = Mock()
        mock_skip.limit.return_value = [mock_analysis_1, mock_analysis_2]
        mock_objects.skip.return_value = mock_skip
        mock_water_analysis.objects = mock_objects
        
        # Make request
        response = client.get("/api/v1/analysis/history")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert "analyses" in data
        assert "total" in data
        assert data["total"] == 2
        assert len(data["analyses"]) == 2
    
    @patch('app.api.history.WaterAnalysis')
    @patch('app.api.history.ObjectId')
    def test_get_analysis_by_id_success(self, mock_objectid, mock_water_analysis):
        """Test successful retrieval of specific analysis by ID"""
        # Mock ObjectId validation
        mock_objectid.is_valid.return_value = True
        
        # Create mock analysis
        mock_analysis = Mock()
        mock_analysis.id = "507f1f77bcf86cd799439011"
        mock_analysis.upload_timestamp = datetime(2026, 2, 5, 12, 0, 0)
        mock_analysis.original_filename = "test.csv"
        mock_analysis.site_name = "Test Site"
        mock_analysis.avg_ph = 7.5
        mock_analysis.ph_category = "Target"
        mock_analysis.avg_tds = 150
        mock_analysis.tds_category = "Moderate"
        mock_analysis.row_count = 10
        mock_analysis.treatment_train = "No treatment required"
        mock_analysis.explanation = "Water is clean"
        
        mock_objects = Mock()
        mock_objects.get.return_value = mock_analysis
        mock_water_analysis.objects = mock_objects
        
        # Make request
        response = client.get("/api/v1/analysis/507f1f77bcf86cd799439011")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["analysis_id"] == "507f1f77bcf86cd799439011"
        assert "summary" in data
        assert "recommendation" in data
    
    @patch('app.api.history.ObjectId')
    def test_get_analysis_by_invalid_id(self, mock_objectid):
        """Test retrieval with invalid ID format"""
        mock_objectid.is_valid.return_value = False
        
        response = client.get("/api/v1/analysis/invalid-id")
        
        assert response.status_code == 400
        assert "Invalid analysis ID format" in response.json()["detail"]
    
    @patch('app.api.history.WaterAnalysis')
    def test_get_history_with_old_records(self, mock_water_analysis):
        """Test history retrieval handles old records without treatment fields"""
        # Mock database query
        mock_objects = Mock()
        mock_objects.count.return_value = 1
        
        # Create mock analysis record WITHOUT treatment fields (old record)
        mock_analysis = Mock(spec=['id', 'upload_timestamp', 'original_filename', 'site_name',
                                     'avg_ph', 'ph_category', 'avg_tds', 'tds_category'])
        mock_analysis.id = "507f1f77bcf86cd799439011"
        mock_analysis.upload_timestamp = datetime(2026, 1, 1, 12, 0, 0)
        mock_analysis.original_filename = "old_test.csv"
        mock_analysis.site_name = "Old Site"
        mock_analysis.avg_ph = 7.5
        mock_analysis.ph_category = "Target"
        mock_analysis.avg_tds = 150
        mock_analysis.tds_category = "Moderate"
        # No treatment_train or explanation attributes (spec prevents auto-generation)
        
        mock_skip = Mock()
        mock_skip.limit.return_value = [mock_analysis]
        mock_objects.skip.return_value = mock_skip
        mock_water_analysis.objects = mock_objects
        
        # Make request
        response = client.get("/api/v1/analysis/history")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert len(data["analyses"]) == 1
        # Should handle missing fields gracefully with None
        assert data["analyses"][0]["treatment_train"] is None
        assert data["analyses"][0]["explanation"] is None
    
    @patch('app.api.history.WaterAnalysis')
    @patch('app.api.history.ObjectId')
    def test_update_analysis_notes_success(self, mock_objectid, mock_water_analysis):
        """Test successful update of analysis notes"""
        # Mock ObjectId validation
        mock_objectid.is_valid.return_value = True
        
        # Create mock analysis
        mock_analysis = Mock()
        mock_analysis.id = "507f1f77bcf86cd799439011"
        mock_analysis.user_notes = None
        
        mock_objects = Mock()
        mock_objects.get.return_value = mock_analysis
        mock_water_analysis.objects = mock_objects
        
        # Make request
        response = client.patch(
            "/api/v1/analysis/507f1f77bcf86cd799439011/notes",
            json={"user_notes": "Used RO system with pre-filtration"}
        )
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["analysis_id"] == "507f1f77bcf86cd799439011"
        assert "user_notes" in data
        mock_analysis.save.assert_called_once()
    
    @patch('app.api.history.ObjectId')
    def test_update_analysis_notes_invalid_id(self, mock_objectid):
        """Test update notes with invalid ID format"""
        mock_objectid.is_valid.return_value = False
        
        response = client.patch(
            "/api/v1/analysis/invalid-id/notes",
            json={"user_notes": "Test notes"}
        )
        
        assert response.status_code == 400
        assert "Invalid analysis ID format" in response.json()["detail"]
