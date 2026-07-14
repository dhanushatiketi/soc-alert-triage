# SOC Alert Triage - Setup Guide

## Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)
- PostgreSQL 14+
- Git

## Quick Start with Docker Compose

### 1. Clone the Repository

```bash
git clone https://github.com/dhanushatiketi/soc-alert-triage.git
cd soc-alert-triage
```

### 2. Configure Environment Variables

```bash
# Copy and update the backend environment file
cp backend/.env.example backend/.env

# Update values as needed
nano backend/.env
```

### 3. Start All Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- Redis cache on port 6379
- FastAPI backend on port 8000
- React frontend on port 3000
- Nginx reverse proxy on ports 80/443
- Prometheus monitoring on port 9090

### 4. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Prometheus:** http://localhost:9090

### 5. Verify Everything is Working

```bash
# Check backend health
curl http://localhost:8000/health

# Check database connection
docker-compose exec postgres psql -U soc_user -d soc_alerts -c "SELECT 1"
```

## Local Development Setup

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup environment:
```bash
cp .env.example .env
```

5. Initialize database:
```bash
alembic upgrade head
```

6. Run development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Setup environment:
```bash
cp .env.example .env
```

4. Start development server:
```bash
npm start
```

Frontend will open at http://localhost:3000

## Troubleshooting

### Port Already in Use

```bash
# Kill process using port
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000   # Windows
```

### Database Connection Error

```bash
# Check PostgreSQL service
docker-compose ps postgres

# View logs
docker-compose logs postgres

# Restart service
docker-compose restart postgres
```

## Next Steps

1. Read [Architecture](./ARCHITECTURE.md)
2. Start creating alerts
3. Integrate with your security tools