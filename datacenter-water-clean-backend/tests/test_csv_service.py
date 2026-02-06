import pytest
import io
from fastapi import UploadFile, HTTPException
from app.services.csv_service import CSVService


@pytest.fixture
def valid_csv_content():
    """Valid CSV content with pH and TDS columns."""
    return b"pH,TDS,Timestamp\n7.2,350,2024-01-01 10:00\n7.5,420,2024-01-01 11:00\n7.8,380,2024-01-01 12:00"


@pytest.fixture
def valid_csv_file(valid_csv_content):
    """Create a mock UploadFile with valid CSV."""
    return UploadFile(
        filename="test.csv",
        file=io.BytesIO(valid_csv_content)
    )


@pytest.fixture
def empty_csv_file():
    """Create a mock UploadFile with empty CSV."""
    return UploadFile(
        filename="empty.csv",
        file=io.BytesIO(b"pH,TDS\n")
    )


@pytest.fixture
def missing_columns_csv():
    """CSV missing required TDS column."""
    return UploadFile(
        filename="missing.csv",
        file=io.BytesIO(b"pH,Temperature\n7.2,25\n7.5,26")
    )


@pytest.mark.asyncio
async def test_validate_csv_success(valid_csv_file):
    """Test successful CSV validation and parsing."""
    df = await CSVService.validate_and_parse_csv(valid_csv_file)
    
    assert not df.empty
    assert len(df) == 3
    assert 'ph' in df.columns
    assert 'tds' in df.columns
    assert df['ph'].iloc[0] == 7.2
    assert df['tds'].iloc[0] == 350


@pytest.mark.asyncio
async def test_validate_csv_empty_file(empty_csv_file):
    """Test validation fails for empty CSV."""
    with pytest.raises(HTTPException) as exc_info:
        await CSVService.validate_and_parse_csv(empty_csv_file)
    
    assert exc_info.value.status_code == 400
    assert "empty" in str(exc_info.value.detail).lower()


@pytest.mark.asyncio
async def test_validate_csv_missing_columns(missing_columns_csv):
    """Test validation fails for missing required columns."""
    with pytest.raises(HTTPException) as exc_info:
        await CSVService.validate_and_parse_csv(missing_columns_csv)
    
    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_csv_case_insensitive_columns():
    """Test that column names are case-insensitive."""
    csv_content = b"PH,tds,TIMESTAMP\n7.2,350,2024-01-01\n"
    file = UploadFile(filename="case.csv", file=io.BytesIO(csv_content))
    
    df = await CSVService.validate_and_parse_csv(file)
    
    assert 'ph' in df.columns
    assert 'tds' in df.columns


def test_calculate_statistics():
    """Test statistics calculation."""
    import pandas as pd
    
    df = pd.DataFrame({
        'ph': [7.0, 7.5, 8.0],
        'tds': [200, 300, 400]
    })
    
    stats = CSVService.calculate_statistics(df)
    
    assert 'avg_ph' in stats
    assert 'avg_tds' in stats
    assert 'row_count' in stats
    assert stats['avg_ph'] == 7.5
    assert stats['avg_tds'] == 300
    assert stats['row_count'] == 3


def test_calculate_statistics_with_nulls():
    """Test statistics calculation handles null values."""
    import pandas as pd
    
    df = pd.DataFrame({
        'ph': [7.0, None, 8.0],
        'tds': [200, 300, None]
    })
    
    stats = CSVService.calculate_statistics(df)
    
    # Should handle null values by dropping rows with any nulls
    assert 'avg_ph' in stats
    assert 'avg_tds' in stats
    assert stats['row_count'] == 1  # Only one row has both pH and TDS values
