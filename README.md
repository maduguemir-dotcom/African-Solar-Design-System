# Solar PV Designer Pro Africa

**Professional solar system design and reporting for Africa and beyond**

## Overview

Solar PV Designer Pro Africa is a comprehensive web application for designing, analyzing, and reporting on solar photovoltaic systems. Built specifically for African markets.

## Features

- ✅ User authentication and account management
- ✅ Project-based solar system design
- ✅ Location-aware solar resource data for African cities
- ✅ Complete system sizing (PV, battery, inverter, charge controller)
- ✅ Financial analysis with ROI and payback calculations
- ✅ Professional PDF report generation

## Quick Start

### 1. Install Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python app/main.py
```

Backend runs at: http://localhost:8000
API Docs: http://localhost:8000/api/docs

### 2. Install Frontend

```bash
cd frontend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Frontend runs at: http://localhost:8501

## License

MIT License

---

**Solar PV Designer Pro Africa** - Empowering solar adoption across Africa ☀️
