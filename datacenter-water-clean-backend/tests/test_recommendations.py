"""
Test recommendation service logic
"""
import pytest
from app.services.recommendation_service import RecommendationService


class TestRecommendationService:
    """Test the recommendation service business logic"""
    
    def test_clean_water_no_treatment(self):
        """Test recommendation for clean water (target pH, low TDS)"""
        treatment, explanation = RecommendationService.get_recommendation(
            avg_ph=7.8, 
            avg_tds=50
        )
        assert treatment == "No treatment required"
        assert "clean" in explanation.lower()
    
    def test_high_ph_low_tds(self):
        """Test recommendation for high pH with low TDS"""
        treatment, explanation = RecommendationService.get_recommendation(
            avg_ph=8.5, 
            avg_tds=80
        )
        assert "H₂SO₄" in treatment or "sulfuric acid" in treatment.lower()
        assert "acid" in explanation.lower()
    
    def test_low_ph_low_tds(self):
        """Test recommendation for low pH with low TDS"""
        treatment, explanation = RecommendationService.get_recommendation(
            avg_ph=7.0, 
            avg_tds=80
        )
        assert "NaOH" in treatment or "sodium hydroxide" in treatment.lower()
        assert "caustic" in explanation.lower() or "naoh" in explanation.lower()
    
    def test_high_tds_target_ph(self):
        """Test recommendation for moderate to high TDS with target pH"""
        treatment, explanation = RecommendationService.get_recommendation(
            avg_ph=7.8, 
            avg_tds=250
        )
        # Should recommend RO or similar treatment for TDS
        assert treatment != "No treatment required"
