# Mala Lingo

A Malayalam language learning app built with Vue 3, FastAPI, and Supabase.

## Quick Start

### Prerequisites
- Docker and Docker Compose
- `.env` file with Supabase credentials

### Environment Setup
1. Create your `.env` file:
```bash
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### Running with Docker

**Development:**
```bash
# Start all services
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.dev.yml down
```

**Production:**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Access Points
- **Frontend**: http://localhost (served by nginx)
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Useful Commands

```bash
# Rebuild containers after code changes
docker-compose down && docker-compose build && docker-compose up -d

# View specific service logs
docker-compose logs -f frontend
docker-compose logs -f backend
docker-compose logs -f sheets-sync

# Clean up containers and volumes
docker-compose down -v
```

## Manual Development (Alternative)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
├── frontend/          # Vue 3 app
├── backend/           # FastAPI backend (refactored modular structure)
├── sheets-sync/       # Google Sheets sync service
├── nginx/             # Nginx configuration
├── docker-compose.yml         # Production
└── docker-compose.dev.yml     # Development
```

## Features

- User authentication with Supabase
- Interactive language lessons
- Word matching games
- Automated Google Sheets data sync
- Dockerized deployment