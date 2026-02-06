from fastapi import APIRouter, HTTPException, Query
from typing import List
from bson import ObjectId
from pydantic import BaseModel, Field

from app.models.water_sample import WaterAnalysis
from app.models.analysis_result import (
    AnalysisHistoryResponse,
    AnalysisHistoryItem,
    AnalysisResponse,
    AnalysisSummary,
    TreatmentRecommendation
)

router = APIRouter(prefix="/api/v1/analysis", tags=["history"])


@router.get("/history", response_model=AnalysisHistoryResponse)
def get_analysis_history(
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records"),
    offset: int = Query(0, ge=0, description="Number of records to skip")
):
    """
    Get history of water quality analyses.
    
    Returns paginated list of past analyses, most recent first.
    """
    # Get total count
    total = WaterAnalysis.objects.count()
    
    # Get paginated results
    analyses = WaterAnalysis.objects.skip(offset).limit(limit)
    
    # Convert to response format
    items = [
        AnalysisHistoryItem(
            id=str(analysis.id),
            upload_timestamp=analysis.upload_timestamp,
            original_filename=analysis.original_filename,
            site_name=analysis.site_name,
            avg_ph=analysis.avg_ph,
            ph_category=analysis.ph_category,
            avg_tds=analysis.avg_tds,
            tds_category=analysis.tds_category,
            treatment_train=getattr(analysis, 'treatment_train', None),
            explanation=getattr(analysis, 'explanation', None),
            user_notes=getattr(analysis, 'user_notes', None)
        )
        for analysis in analyses
    ]
    
    return AnalysisHistoryResponse(
        analyses=items,
        total=total,
        limit=limit,
        offset=offset
    )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis_by_id(analysis_id: str):
    """
    Get specific analysis by ID.
    
    Returns full analysis details including recommendation.
    """
    # Validate ObjectId format
    if not ObjectId.is_valid(analysis_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid analysis ID format"
        )
    
    # Query database
    try:
        analysis = WaterAnalysis.objects.get(id=analysis_id)
    except WaterAnalysis.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Analysis not found",
                "analysis_id": analysis_id
            }
        )
    
    # Return response
    return AnalysisResponse(
        analysis_id=str(analysis.id),
        upload_timestamp=analysis.upload_timestamp,
        original_filename=analysis.original_filename,
        site_name=analysis.site_name,
        summary=AnalysisSummary(
            avg_ph=analysis.avg_ph,
            ph_category=analysis.ph_category,
            avg_tds=analysis.avg_tds,
            tds_category=analysis.tds_category,
            row_count=analysis.row_count
        ),
        recommendation=TreatmentRecommendation(
            treatment_train=analysis.treatment_train,
            explanation=analysis.explanation
        )
    )


class UpdateNotesRequest(BaseModel):
    """Request model for updating user notes."""
    user_notes: str = Field(..., max_length=2000, description="User notes about methods actually used")


@router.patch("/{analysis_id}/notes")
def update_analysis_notes(analysis_id: str, request: UpdateNotesRequest):
    """
    Update user notes for a specific analysis.
    
    Allows users to add notes about the treatment methods they actually used.
    """
    # Validate ObjectId format
    if not ObjectId.is_valid(analysis_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid analysis ID format"
        )
    
    # Query database
    try:
        analysis = WaterAnalysis.objects.get(id=analysis_id)
    except WaterAnalysis.DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Analysis not found",
                "analysis_id": analysis_id
            }
        )
    
    # Update notes
    analysis.user_notes = request.user_notes
    analysis.save()
    
    return {
        "success": True,
        "analysis_id": str(analysis.id),
        "user_notes": analysis.user_notes
    }
