import pandas as pd
import io
from typing import Tuple, Dict, Any
from fastapi import UploadFile, HTTPException


class CSVService:
    """Service for CSV file processing."""
    
    REQUIRED_COLUMNS = ['pH', 'TDS']
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    async def validate_and_parse_csv(file: UploadFile) -> pd.DataFrame:
        """
        Validate and parse CSV file.
        
        Args:
            file: Uploaded CSV file
            
        Returns:
            Parsed DataFrame
            
        Raises:
            HTTPException: If validation fails
        """
        # Check file size
        contents = await file.read()
        if len(contents) > CSVService.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is {CSVService.MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        # Reset file pointer
        await file.seek(0)
        
        # Try to parse CSV
        try:
            df = pd.read_csv(io.BytesIO(contents))
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to parse CSV file: {str(e)}"
            )
        
        # Check if DataFrame is empty
        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="CSV file is empty"
            )
        
        # Normalize column names (case-insensitive)
        df.columns = df.columns.str.strip().str.lower()
        
        # Check for required columns
        missing_columns = []
        for col in CSVService.REQUIRED_COLUMNS:
            if col.lower() not in df.columns:
                missing_columns.append(col)
        
        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Missing required columns",
                    "details": f"CSV must contain 'pH' and 'TDS' columns",
                    "missing_columns": missing_columns
                }
            )
        
        return df
    
    @staticmethod
    def calculate_statistics(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate water quality statistics from DataFrame.
        
        Args:
            df: DataFrame with pH and TDS columns
            
        Returns:
            Dictionary with calculated statistics
        """
        # Get pH and TDS columns
        ph_col = 'ph'
        tds_col = 'tds'
        
        # Convert to numeric, coercing errors to NaN
        df[ph_col] = pd.to_numeric(df[ph_col], errors='coerce')
        df[tds_col] = pd.to_numeric(df[tds_col], errors='coerce')
        
        # Drop rows with NaN values
        df_clean = df[[ph_col, tds_col]].dropna()
        
        if df_clean.empty:
            raise HTTPException(
                status_code=400,
                detail="No valid numeric data found in pH or TDS columns"
            )
        
        # Calculate averages
        avg_ph = float(df_clean[ph_col].mean())
        avg_tds = float(df_clean[tds_col].mean())
        
        # Determine categories
        ph_category = CSVService._get_ph_category(avg_ph)
        tds_category = CSVService._get_tds_category(avg_tds)
        
        # Optional: Calculate min/max
        min_ph = float(df_clean[ph_col].min())
        max_ph = float(df_clean[ph_col].max())
        min_tds = float(df_clean[tds_col].min())
        max_tds = float(df_clean[tds_col].max())
        
        return {
            'avg_ph': avg_ph,
            'ph_category': ph_category,
            'avg_tds': avg_tds,
            'tds_category': tds_category,
            'row_count': len(df_clean),
            'min_ph': min_ph,
            'max_ph': max_ph,
            'min_tds': min_tds,
            'max_tds': max_tds
        }
    
    @staticmethod
    def _get_ph_category(ph: float) -> str:
        """Determine pH category."""
        if ph <= 7.5:
            return "Low pH"
        elif ph < 8.3:
            return "In target range"
        else:
            return "High pH"
    
    @staticmethod
    def _get_tds_category(tds: float) -> str:
        """Determine TDS category."""
        if tds < 100:
            return "Low"
        elif tds < 300:
            return "Moderate"
        else:
            return "High"
