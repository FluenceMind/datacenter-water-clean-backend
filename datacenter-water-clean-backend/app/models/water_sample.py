from mongoengine import Document, StringField, FloatField, DateTimeField, IntField
from datetime import datetime
from typing import Optional


class WaterAnalysis(Document):
    """MongoDB document for water quality analysis results."""
    
    # File information
    upload_timestamp = DateTimeField(required=True, default=datetime.utcnow)
    original_filename = StringField(required=True, max_length=255)
    site_name = StringField(max_length=255)
    
    # Calculated statistics
    avg_ph = FloatField(required=True)
    ph_category = StringField(required=True, choices=[
        "Low pH",
        "In target range",
        "High pH"
    ])
    avg_tds = FloatField(required=True)
    tds_category = StringField(required=True, choices=[
        "Low",
        "Moderate",
        "High"
    ])
    
    # Recommendation
    treatment_train = StringField(required=True, max_length=500)
    explanation = StringField(required=True, max_length=2000)
    
    # User notes about methods actually used
    user_notes = StringField(max_length=2000)
    
    # Metadata
    created_at = DateTimeField(default=datetime.utcnow)
    row_count = IntField(required=True, min_value=1)
    
    # Optional: Additional statistics
    min_ph = FloatField()
    max_ph = FloatField()
    min_tds = FloatField()
    max_tds = FloatField()
    
    meta = {
        'collection': 'water_analyses',
        'indexes': [
            '-upload_timestamp',  # Descending index for recent first
            'site_name',
            'created_at'
        ],
        'ordering': ['-upload_timestamp']
    }
    
    def to_dict(self) -> dict:
        """Convert document to dictionary for API response."""
        return {
            'id': str(self.id),
            'upload_timestamp': self.upload_timestamp.isoformat(),
            'original_filename': self.original_filename,
            'site_name': self.site_name,
            'summary': {
                'avg_ph': round(self.avg_ph, 2),
                'ph_category': self.ph_category,
                'avg_tds': round(self.avg_tds, 2),
                'tds_category': self.tds_category,
                'row_count': self.row_count
            },
            'recommendation': {
                'treatment_train': self.treatment_train,
                'explanation': self.explanation
            },
            'created_at': self.created_at.isoformat()
        }
