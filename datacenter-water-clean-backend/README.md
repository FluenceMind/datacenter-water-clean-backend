# DataCenter Water Clean

A web application for analyzing water quality in datacenter cooling systems. Upload CSV files with pH and TDS measurements, get treatment recommendations based on predefined rules, and track analysis history over time.

## What It Does

This application helps datacenter operators monitor water quality and determine what treatment methods to use. You upload a CSV file with pH and TDS measurements, and the system applies a rule-based logic to recommend appropriate treatment steps. Each analysis is stored so you can review past results and add notes about what treatment you actually applied.

The analysis uses fixed thresholds:
- **pH target range:** 7.5 - 8.3
- **TDS categories:** Low (<100 mg/L), Moderate (100-299 mg/L), High (≥300 mg/L)

Based on these values, the system selects from 9 predefined treatment rules (A through I). Each rule maps to a specific treatment train like "pH adjustment with NaOH → Reverse osmosis (RO)" and includes an explanation of why that method was selected.

### Complete Treatment Rules

| Rule | pH Category | TDS Category | Treatment |
|------|------------|--------------|-----------|
| **A** | Target | Low | No treatment required |
| **B** | High | Low | pH adjustment with H₂SO₄ |
| **C** | Low | Low | pH adjustment with NaOH |
| **D** | Target | Moderate | Reverse osmosis (RO) |
| **E** | Target | High | Ion exchange |
| **F** | High | Moderate | H₂SO₄ → RO |
| **G** | Low | Moderate | NaOH → RO |
| **H** | High | High | H₂SO₄ → Ion exchange |
| **I** | Low | High | NaOH → Ion exchange |

## Features

- Upload CSV files with water quality measurements (pH, TDS)
- Get treatment recommendations based on rule-based logic
- View analysis history with pagination
- Add notes to track what treatment methods were actually used
- Optional site name for each analysis
- RESTful API backend with data validation
- Responsive web interface

## Tech Stack

**Backend:**
- Python 3.12
- FastAPI (web framework)
- MongoDB (database)
- Pandas (CSV processing)
- Pydantic (data validation)

**Frontend:**
- React 19
- Material-UI (components)
- Vite (build tool)
- React Router (routing)
- Axios (HTTP client)

## Dependencies

### Backend (Python)

```
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
python-multipart>=0.0.17
mongoengine>=0.29.0
pymongo>=4.10.1
pandas>=2.2.0
numpy>=2.0.0
python-dotenv>=1.0.0
pydantic>=2.10.0
pytest>=8.0.0
```

### Frontend (JavaScript)

```
react: ^19.2.0
react-dom: ^19.2.0
react-router-dom: ^7.13.0
@mui/material: ^7.3.7
@mui/icons-material: ^7.3.7
axios: ^1.13.4
vite: ^7.2.4
```

## Setup Instructions

### Prerequisites

- Python 3.12 or higher
- Node.js 18 or higher
- MongoDB instance (local or cloud)

### Backend Setup

1. Navigate to the backend directory:
```
cd datacenter-water-clean-backend
```

2. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create a `.env` file with your MongoDB connection string:
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/dbname
```

5. Run the development server:
```
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```
cd frontend
```

2. Install dependencies:
```
npm install
```

3. Create a `.env` file with the backend URL:
```
VITE_API_URL=http://localhost:8000
```

4. Run the development server:
```
npm run dev
```

The app will be available at `http://localhost:5173`

### Running Tests

Backend tests:
```bash
cd datacenter-water-clean-backend
pytest
```

## CSV File Format

The application expects CSV files with the following columns:
- `pH` - pH measurements (numeric)
- `TDS` - Total Dissolved Solids in mg/L (numeric)

Example:
```csv
pH,TDS
7.2,150
7.3,148
7.1,155
```

## Deployment

- **Backend:** Deployed on Render
- **Frontend:** Deployed on Vercel
- **Database:** MongoDB Atlas

## License

See LICENSE file for details.

## Author 
This project is developed by Tatiana