# SOC Alert Triage System

A comprehensive Security Operations Center (SOC) alert triage platform for ingesting, classifying, routing, and managing security alerts from multiple sources.

## Features

- 🚨 **Multi-source Alert Ingestion** - Ingest alerts from various security tools and platforms
- 🏷️ **Intelligent Classification** - Automatically classify and categorize alerts
- 📊 **Real-time Dashboard** - Monitor and triage alerts in real-time
- 🔀 **Smart Routing** - Route alerts to appropriate teams based on rules
- 🎯 **Alert Enrichment** - Enrich alerts with contextual information
- 📈 **Analytics & Reporting** - Track metrics and generate reports
- 🔗 **Integration Ready** - Easy integration with ticketing systems (Jira, ServiceNow)
- 👥 **Role-based Access Control** - Manage permissions and access levels

## Tech Stack

- **Backend:** Python 3.11+ with FastAPI
- **Frontend:** React 18+ with TypeScript
- **Database:** PostgreSQL 14+
- **Message Queue:** Redis
- **Containerization:** Docker & Docker Compose
- **API Documentation:** Swagger/OpenAPI

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/dhanushatiketi/soc-alert-triage.git
cd soc-alert-triage

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Database: localhost:5432
```

### Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
alembic upgrade head

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env

# Start development server
npm start
```

## Project Structure

```
soc-alert-triage/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── core/           # Core configurations
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── api/            # API routes
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Utilities
│   │   └── main.py         # Application entry point
│   ├── migrations/         # Alembic migrations
│   ├── tests/             # Test files
│   ├── requirements.txt   # Python dependencies
│   ├── .env.example       # Example environment file
│   └── Dockerfile
│
├── frontend/              # React TypeScript frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── store/         # State management
│   │   ├── types/         # TypeScript types
│   │   ├── styles/        # CSS/SCSS
│   │   └── App.tsx        # Main App component
│   ├── public/            # Static files
│   ├── package.json       # Node dependencies
│   ├── .env.example       # Example environment file
│   └── Dockerfile
│
├── docker-compose.yml     # Docker Compose configuration
├── nginx/                 # Nginx configuration
├── docs/                  # Documentation
└── scripts/              # Utility scripts
```

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` to access the interactive Swagger API documentation.

### Key Endpoints

- `POST /api/v1/alerts` - Submit new alert
- `GET /api/v1/alerts` - List alerts with filtering
- `GET /api/v1/alerts/{id}` - Get alert details
- `PUT /api/v1/alerts/{id}` - Update alert status
- `GET /api/v1/alerts/stats` - Get alert statistics
- `POST /api/v1/rules` - Create triage rule
- `GET /api/v1/teams` - List teams
- `POST /api/v1/escalate/{id}` - Escalate alert

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/soc_alerts
SQLALCHEMY_ECHO=False

# Application
APP_NAME=SOC Alert Triage
DEBUG=True
SECRET_KEY=your-secret-key-here

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Email
SMTP_ENABLED=False
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

## Usage Examples

### Submitting an Alert

```bash
curl -X POST http://localhost:8000/api/v1/alerts \
  -H "Content-Type: application/json" \
  -d '{
    "source": "firewall",
    "severity": "high",
    "title": "Suspicious Login Attempt",
    "description": "Multiple failed login attempts detected",
    "metadata": {
      "source_ip": "192.168.1.100",
      "target_system": "prod-db-01"
    }
  }'
```

### Getting Alert Statistics

```bash
curl http://localhost:8000/api/v1/alerts/stats/summary?time_period=24h
```

## Development

### Running Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Code Quality

```bash
# Format code
black app/

# Lint
pylint app/

# Type checking
mypy app/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Deployment

### Docker Hub

```bash
docker build -t dhanushatiketi/soc-alert-triage:latest .
docker push dhanushatiketi/soc-alert-triage:latest
```

### Kubernetes

See `docs/kubernetes-deployment.md` for detailed deployment instructions.

## Monitoring & Logging

- **Application Logs:** Check `logs/` directory
- **Prometheus Metrics:** `http://localhost:9090`
- **ELK Stack:** Available for centralized logging

## Support & Documentation

- 📖 [Full Documentation](./docs/)
- 🐛 [Report Issues](https://github.com/dhanushatiketi/soc-alert-triage/issues)
- 💬 [Discussions](https://github.com/dhanushatiketi/soc-alert-triage/discussions)

## License

MIT License - see LICENSE file for details

## Authors

- Dhanush Atiketi

## Acknowledgments

- FastAPI community
- React community
- PostgreSQL community

---

**Last Updated:** 2026-07-14