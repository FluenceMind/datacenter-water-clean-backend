# DataCenter Water Clean - Backend API

FastAPI-based backend for water quality analysis and treatment recommendations.

## ✅ Implemented Features

### Core Functionality
- **CSV Upload & Analysis**: Upload water quality data (pH, TDS) for automated analysis
- **Treatment Recommendations**: 9 intelligent rules based on pH/TDS combinations
- **Analysis History**: View past analyses with pagination
- **MongoDB Integration**: Persistent storage of all analyses
- **RESTful API**: Clean, documented endpoints with Swagger UI

### Water Quality Parameters
- **pH**: Target range 7.5-8.3
  - Low: ≤ 7.5
  - Target: 7.5-8.3
  - High: ≥ 8.3

- **TDS (Total Dissolved Solids)**: Measured in mg/L or ppm
  - Low: < 100
  - Moderate: 100-299
  - High: ≥ 300

### Treatment Rules
| pH Category | TDS Category | Treatment |
|------------|--------------|-----------|
| Target | Low | No treatment required |
| High | Low | pH adjustment with H₂SO₄ |
| Low | Low | pH adjustment with NaOH |
| Target | Moderate | Reverse osmosis (RO) |
| Target | High | Ion exchange |
| High | Moderate | H₂SO₄ → RO |
| Low | Moderate | NaOH → RO |
| High | High | H₂SO₄ → Ion exchange |
| Low | High | NaOH → Ion exchange |

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- MongoDB Atlas account (free tier)

### Installation

1. **Clone and navigate to backend**:
   ```bash
   cd datacenter-water-clean-backend
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   Create `.env` file with:
   ```env
   MONGODB_URL=your_mongodb_connection_string
   MONGODB_DB_NAME=water_quality
   API_HOST=0.0.0.0
   API_PORT=8000
   CORS_ORIGINS=http://localhost:3000,http://localhost:5173
   ENVIRONMENT=development
   ```

5. **Run the server**:
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Access API documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

## 📡 API Endpoints

### Health Check
```
GET /health
```
Returns server status.

### Upload & Analyze
```
POST /api/v1/analysis/upload
Content-Type: multipart/form-data

Parameters:
- file: CSV file (required) - must contain 'pH' and 'TDS' columns
- site_name: string (optional) - site identifier

Response:
{
  "analysis_id": "string",
  "upload_timestamp": "datetime",
  "original_filename": "string",
  "site_name": "string",
  "summary": {
    "avg_ph": 7.84,
    "ph_category": "In target range",
    "avg_tds": 187.6,
    "tds_category": "Moderate",
    "row_count": 5
  },
  "recommendation": {
    "treatment_train": "Reverse osmosis (RO)",
    "explanation": "TDS is elevated; RO is recommended..."
  }
}
```

### Get Analysis History
```
GET /api/v1/analysis/history?limit=20&offset=0

Response:
{
  "analyses": [...],
  "total": 3,
  "limit": 20,
  "offset": 0
}
```

### Get Analysis by ID
```
GET /api/v1/analysis/{analysis_id}

Response: Same as upload response
```

## 🧪 Testing

### Run automated tests:
```bash
cd datacenter-water-clean
python test_api.py
```

### Sample CSV format:
```csv
pH,TDS,Location,Timestamp
7.2,85,Server Room A,2024-01-15 08:00:00
7.4,92,Server Room A,2024-01-15 09:00:00
```

Test samples are available in `../test_samples/` directory.

## 📁 Project Structure

```
datacenter-water-clean-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app & startup
│   ├── api/
│   │   ├── __init__.py
│   │   ├── analysis.py            # Upload endpoint
│   │   ├── health.py              # Health check
│   │   └── history.py             # History endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              # Settings & configuration
│   ├── db/
│   │   ├── __init__.py
│   │   └── mongo.py               # MongoDB connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── analysis_result.py     # Pydantic models
│   │   └── water_sample.py        # MongoDB document
│   └── services/
│       ├── __init__.py
│       ├── csv_service.py         # CSV parsing & validation
│       └── recommendation_service.py  # Treatment logic
├── requirements.txt
├── .env                           # Environment variables
├── .gitignore
└── README.md
```

## 🛠️ Technologies

- **FastAPI** 0.115+ - Modern web framework
- **MongoDB** - Document database (via MongoEngine ODM)
- **Pandas** 2.2+ - Data processing
- **Pydantic** 2.10+ - Data validation
- **Uvicorn** - ASGI server

## 🌐 Deployment

### Render (Recommended)
1. Create new Web Service
2. Connect GitHub repository
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `.env`
5. Deploy!

Free tier available: https://render.com

## 📊 Database Schema

### WaterAnalysis Collection
```python
{
  "_id": ObjectId,
  "upload_timestamp": datetime,
  "original_filename": str,
  "site_name": str (optional),
  "avg_ph": float,
  "ph_category": str,
  "avg_tds": float,
  "tds_category": str,
  "treatment_train": str,
  "explanation": str,
  "row_count": int,
  "min_ph": float,
  "max_ph": float,
  "min_tds": float,
  "max_tds": float,
  "created_at": datetime
}
```

## 🔧 Development

### Add new endpoint:
1. Create route in `app/api/`
2. Import and include in `app/main.py`
3. Test via Swagger UI

### Add new service:
1. Create service in `app/services/`
2. Import and use in API routes

### Update models:
1. MongoDB documents: `app/models/water_sample.py`
2. API responses: `app/models/analysis_result.py`

## 📝 Next Steps (Frontend Integration)

The backend is ready for frontend integration. Frontend should:
1. Use React with Vite
2. Implement Material-UI for components
3. Create forms for file upload
4. Display analysis results and history
5. Visualize data with charts (pH/TDS trends)

See `PROJECT_REQUIREMENTS.md` and `IMPLEMENTATION_PLAN.md` for details.

## 🤝 Contributing

This is a capstone project for App Academy by Tatiana Didenko.

## 📄 License

See LICENSE file for details.
