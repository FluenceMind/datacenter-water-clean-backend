#!/usr/bin/env python3
"""
Test script for DataCenter Water Clean API
Tests all major endpoints with sample CSV data.
"""
import requests
import sys
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200

def test_upload(csv_file_path, site_name=None):
    """Test CSV upload and analysis."""
    print(f"Testing upload with {csv_file_path}...")
    
    with open(csv_file_path, 'rb') as f:
        files = {'file': (Path(csv_file_path).name, f, 'text/csv')}
        data = {}
        if site_name:
            data['site_name'] = site_name
        
        response = requests.post(f"{BASE_URL}/api/v1/analysis/upload", files=files, data=data)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Analysis ID: {result['analysis_id']}")
        print(f"Filename: {result['original_filename']}")
        print(f"Site: {result.get('site_name', 'N/A')}")
        print(f"Summary:")
        print(f"  - Avg pH: {result['summary']['avg_ph']:.2f} ({result['summary']['ph_category']})")
        print(f"  - Avg TDS: {result['summary']['avg_tds']:.2f} mg/L ({result['summary']['tds_category']})")
        print(f"  - Samples: {result['summary']['row_count']}")
        print(f"Recommendation:")
        print(f"  - Treatment: {result['recommendation']['treatment_train']}")
        print(f"  - Explanation: {result['recommendation']['explanation']}")
        print()
        return result['analysis_id']
    else:
        print(f"Error: {response.text}\n")
        return None

def test_history():
    """Test history endpoint."""
    print("Testing /api/v1/analysis/history endpoint...")
    response = requests.get(f"{BASE_URL}/api/v1/analysis/history")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Total analyses: {result['total']}")
        print(f"Returned: {len(result['analyses'])} records")
        for analysis in result['analyses'][:3]:  # Show first 3
            print(f"  - {analysis['original_filename']}: pH={analysis['avg_ph']:.2f}, TDS={analysis['avg_tds']:.2f}")
        print()
        return True
    else:
        print(f"Error: {response.text}\n")
        return False

def test_get_by_id(analysis_id):
    """Test get analysis by ID."""
    print(f"Testing /api/v1/analysis/{analysis_id} endpoint...")
    response = requests.get(f"{BASE_URL}/api/v1/analysis/{analysis_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Retrieved analysis: {result['original_filename']}")
        print(f"Treatment: {result['recommendation']['treatment_train']}\n")
        return True
    else:
        print(f"Error: {response.text}\n")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("DataCenter Water Clean API Test Suite")
    print("=" * 60)
    print()
    
    # Test health
    if not test_health():
        print("❌ Health check failed!")
        sys.exit(1)
    print("✅ Health check passed!\n")
    
    # Test uploads
    test_files = [
        ("test_samples/sample_water_data.csv", "Server Room A"),
        ("test_samples/high_ph_high_tds.csv", "Cooling Tower B"),
        ("test_samples/moderate_tds_target_ph.csv", "Data Center 1"),
    ]
    
    analysis_ids = []
    for csv_file, site in test_files:
        csv_path = Path(__file__).parent / csv_file
        if csv_path.exists():
            analysis_id = test_upload(str(csv_path), site)
            if analysis_id:
                analysis_ids.append(analysis_id)
                print("✅ Upload test passed!\n")
            else:
                print("❌ Upload test failed!\n")
        else:
            print(f"⚠️  Test file not found: {csv_path}\n")
    
    # Test history
    if test_history():
        print("✅ History test passed!\n")
    else:
        print("❌ History test failed!\n")
    
    # Test get by ID
    if analysis_ids:
        if test_get_by_id(analysis_ids[0]):
            print("✅ Get by ID test passed!\n")
        else:
            print("❌ Get by ID test failed!\n")
    
    print("=" * 60)
    print("Test suite completed!")
    print(f"API Documentation: {BASE_URL}/docs")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is the server running at http://localhost:8000?")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        sys.exit(1)
