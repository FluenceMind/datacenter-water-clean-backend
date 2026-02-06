from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from datetime import datetime, UTC

from app.services.csv_service import CSVService
from app.services.recommendation_service import RecommendationService
from app.models.water_sample import WaterAnalysis
from app.models.analysis_result import AnalysisResponse, AnalysisSummary, TreatmentRecommendation

router = APIRouter(prefix="/api/v1/analysis", tags=["analysis"])


@router.post("/upload", response_model=AnalysisResponse)
async def upload_and_analyze(
    file: UploadFile = File(..., description="CSV file with water quality data"),
    site_name: Optional[str] = Form(None, description="Optional site identifier")
):
    """
    Upload CSV file and perform water quality analysis.
    
    Returns analysis results with treatment recommendation.
    """
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only CSV files are accepted."
        )
    
    # Parse and validate CSV
    df = await CSVService.validate_and_parse_csv(file)
    
    # Calculate statistics
    stats = CSVService.calculate_statistics(df)
    
    # Get treatment recommendation
    treatment_train, explanation = RecommendationService.get_recommendation(
        stats['avg_ph'],
        stats['avg_tds']
    )
    
    # Save to database
    analysis = WaterAnalysis(
        upload_timestamp=datetime.now(UTC),
        original_filename=file.filename,
        site_name=site_name,
        avg_ph=stats['avg_ph'],
        ph_category=stats['ph_category'],
        avg_tds=stats['avg_tds'],
        tds_category=stats['tds_category'],
        treatment_train=treatment_train,
        explanation=explanation,
        row_count=stats['row_count'],
        min_ph=stats.get('min_ph'),
        max_ph=stats.get('max_ph'),
        min_tds=stats.get('min_tds'),
        max_tds=stats.get('max_tds')
    )
    analysis.save()
    
    # Return response
    return AnalysisResponse(
        analysis_id=str(analysis.id),
        upload_timestamp=analysis.upload_timestamp,
        original_filename=analysis.original_filename,
        site_name=analysis.site_name,
        summary=AnalysisSummary(
            avg_ph=stats['avg_ph'],
            ph_category=stats['ph_category'],
            avg_tds=stats['avg_tds'],
            tds_category=stats['tds_category'],
            row_count=stats['row_count']
        ),
        recommendation=TreatmentRecommendation(
            treatment_train=treatment_train,
            explanation=explanation
        )
    )
