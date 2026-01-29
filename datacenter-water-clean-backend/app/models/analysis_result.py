from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AnalysisSummary(BaseModel):
    """Summary statistics from water analysis."""
    avg_ph: float = Field(..., description="Average pH value")
    ph_category: str = Field(..., description="pH category")
    avg_tds: float = Field(..., description="Average TDS in mg/L")
    tds_category: str = Field(..., description="TDS category")
    row_count: int = Field(..., description="Number of samples analyzed")


class TreatmentRecommendation(BaseModel):
    """Treatment recommendation details."""
    treatment_train: str = Field(..., description="Recommended treatment steps")
    explanation: str = Field(..., description="Explanation of recommendation")


class AnalysisResponse(BaseModel):
    """API response for water analysis."""
    analysis_id: str = Field(..., description="Unique analysis ID")
    upload_timestamp: datetime = Field(..., description="When file was uploaded")
    original_filename: str = Field(..., description="Original CSV filename")
    site_name: Optional[str] = Field(None, description="Optional site identifier")
    summary: AnalysisSummary
    recommendation: TreatmentRecommendation


class AnalysisHistoryItem(BaseModel):
    """Compact analysis record for history list."""
    id: str
    upload_timestamp: datetime
    original_filename: str
    site_name: Optional[str]
    avg_ph: float
    ph_category: str
    avg_tds: float
    tds_category: str


class AnalysisHistoryResponse(BaseModel):
    """API response for analysis history."""
    analyses: list[AnalysisHistoryItem]
    total: int
    limit: int
    offset: int
