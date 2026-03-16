# ScholyBud Backend API

FastAPI-based backend for ScholyBud - a multi-tenant school management SaaS system.

## Project Setup

### Prerequisites
- Python 3.11 or higher
- PostgreSQL database
- pip or poetry for package management

### Installation

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -e ".[dev]"
```

3. Copy environment variables:
```bash
cp .env.example .env
```

4. Update `.env` with your configuration

## Running the Application

### Development Server
```bash
uvicorn main:app --reload
```

### Production Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Running Tests

```bash
pytest
```

## Project Structure

```
backend/
├── main.py              # Application entry point
├── pyproject.toml       # Project configuration
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore patterns
└── README.md           # This file
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLModel** - SQL toolkit and ORM
- **PostgreSQL** - Database
- **Pydantic** - Data validation using Python type annotations
- **python-jose** - JWT token handling
- **passlib** - Password hashing

## Development

### Code Quality
```bash
# Linting
ruff check .

# Formatting
ruff format .

# Type checking
mypy .
```

### Environment Variables

See `.env.example` for all available configuration options.
