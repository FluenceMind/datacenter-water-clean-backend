import pytest
from app.services.recommendation_service import RecommendationService


def test_recommendation_moderate_tds_high_ph():
    """Test Rule F: Moderate TDS, High pH."""
    treatment, explanation = RecommendationService.get_recommendation(
        avg_ph=8.5,  # High pH
        avg_tds=200  # Moderate TDS
    )
    
    assert "H₂SO₄" in treatment
    assert "RO" in treatment
    assert "acid" in explanation.lower()


def test_recommendation_moderate_tds_low_ph():
    """Test Rule G: Moderate TDS, Low pH."""
    treatment, explanation = RecommendationService.get_recommendation(
        avg_ph=7.0,  # Low pH
        avg_tds=200  # Moderate TDS
    )
    
    assert "NaOH" in treatment
    assert "RO" in treatment
    assert "caustic" in explanation.lower()


def test_recommendation_high_tds_high_ph():
    """Test Rule H: High TDS, High pH."""
    treatment, explanation = RecommendationService.get_recommendation(
        avg_ph=8.5,  # High pH
        avg_tds=500  # High TDS
    )
    
    assert "H₂SO₄" in treatment
    assert "Ion exchange" in treatment
    assert "acid" in explanation.lower()


def test_recommendation_high_tds_low_ph():
    """Test Rule I: High TDS, Low pH."""
    treatment, explanation = RecommendationService.get_recommendation(
        avg_ph=7.0,  # Low pH
        avg_tds=500  # High TDS
    )
    
    assert "NaOH" in treatment
    assert "Ion exchange" in treatment
    assert "caustic" in explanation.lower()


def test_recommendation_clean_water():
    """Test Rule A: Clean water, no treatment needed."""
    treatment, explanation = RecommendationService.get_recommendation(
        avg_ph=8.0,  # Target pH
        avg_tds=50   # Low TDS
    )
    
    assert "No treatment required" in treatment
    assert "clean" in explanation.lower()


def test_recommendation_high_ph_low_tds():
    """Test Rule B: High pH, Low TDS."""
    treatment, explanation = RecommendationService.get_recommendation(
        avg_ph=8.5,  # High pH
        avg_tds=50   # Low TDS
    )
    
    assert "H₂SO₄" in treatment
    assert "acid" in explanation.lower()


def test_recommendation_low_ph_low_tds():
    """Test Rule C: Low pH, Low TDS."""
    treatment, explanation = RecommendationService.get_recommendation(
        avg_ph=7.0,  # Low pH
        avg_tds=50   # Low TDS
    )
    
    assert "NaOH" in treatment
    assert "caustic" in explanation.lower()


def test_recommendation_moderate_tds_target_ph():
    """Test Rule D: Moderate TDS, Target pH."""
    treatment, explanation = RecommendationService.get_recommendation(
        avg_ph=8.0,  # Target pH
        avg_tds=200  # Moderate TDS
    )
    
    assert "Reverse osmosis" in treatment
    assert "RO" in treatment


def test_recommendation_high_tds_target_ph():
    """Test Rule E: High TDS, Target pH."""
    treatment, explanation = RecommendationService.get_recommendation(
        avg_ph=8.0,  # Target pH
        avg_tds=500  # High TDS
    )
    
    assert "Ion exchange" in treatment
    assert "dissolved ions" in explanation.lower()


def test_recommendation_boundary_ph_low():
    """Test pH exactly at low boundary (7.5)."""
    treatment, explanation = RecommendationService.get_recommendation(
        avg_ph=7.5,  # Exactly at boundary
        avg_tds=50
    )
    
    # Should trigger low pH treatment
    assert "NaOH" in treatment


def test_recommendation_boundary_ph_high():
    """Test pH exactly at high boundary (8.3)."""
    treatment, explanation = RecommendationService.get_recommendation(
        avg_ph=8.3,  # Exactly at boundary
        avg_tds=50
    )
    
    # Should trigger high pH treatment
    assert "H₂SO₄" in treatment


def test_recommendation_boundary_tds_low():
    """Test TDS at low boundary (100)."""
    treatment, explanation = RecommendationService.get_recommendation(
        avg_ph=8.0,
        avg_tds=100  # Exactly at boundary
    )
    
    # Should be moderate TDS
    assert "RO" in treatment


def test_recommendation_boundary_tds_high():
    """Test TDS at high boundary (300)."""
    treatment, explanation = RecommendationService.get_recommendation(
        avg_ph=8.0,
        avg_tds=300  # Exactly at boundary
    )
    
    # Should be high TDS
    assert "Ion exchange" in treatment
