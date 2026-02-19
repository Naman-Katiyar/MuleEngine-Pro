# MuleEngine-Pro

A comprehensive analysis and visualization system for detecting patterns and relationships in transactional data.

## Overview

MuleEngine-Pro is a full-stack application designed to analyze and visualize complex transaction networks. It combines a powerful backend API with an intuitive frontend interface for pattern detection and graph analysis.

## Features

- **Transaction Analysis**: Process and analyze large CSV datasets of transactions
- **Pattern Detection**: Identify suspicious patterns and anomalies in transaction networks
- **Graph Visualization**: Interactive network graphs showing relationships and connections
- **Real-time Statistics**: Comprehensive analytics and scoring metrics
- **Data Export**: Export analysis results in multiple formats

## Project Structure

```
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI application entry
│   │   ├── core/           # Core configuration and scoring
│   │   ├── models/         # Data schemas
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   └── requirements.txt     # Python dependencies
├── frontend/               # React.js frontend
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── components/     # React components
│   │   └── index.js        # Entry point
│   └── package.json        # Node.js dependencies
├── data/                   # Sample CSV datasets
└── render.yaml             # Deployment configuration
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Installation

#### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

#### Frontend Setup

```bash
cd frontend
npm install
```

### Running Locally

#### Start Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload
```

Server will run at `http://localhost:8000`

#### Start Frontend Server

```bash
cd frontend
npm start
```

Application will open at `http://localhost:3000`

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

## Deployment

This application is configured for deployment on Render. See `render.yaml` for configuration details.

### Deploy to Render

1. Push code to GitHub
2. Connect repository to Render
3. Configure build and start commands:
   - **Build**: `pip install -r backend/requirements.txt`
   - **Start**: `cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`

## Data Format

The application accepts CSV files with transaction data. Sample data is provided in the `data/` directory.

Example CSV format:

- Transaction ID
- Sender/Recipient
- Amount
- Timestamp
- Transaction Type

## Configuration

Environment variables can be set in `.env` file. Copy `.env.example` to `.env` and update values:

```
DATABASE_URL=your_database_url
LOG_LEVEL=info
```

## Testing

Run test suites:

```bash
python test_implementations.py
python test_performance.py
python test_scaling.py
```

## Technologies Used

### Backend

- FastAPI
- Python 3
- Pandas
- NetworkX

### Frontend

- React.js
- Tailwind CSS
- JavaScript

### Deployment

- Render (Cloud Platform)

## License

Proprietary - All rights reserved

## Contributing

For questions or contributions, please contact the development team.

## Support

For issues and questions, please open an issue on GitHub.
