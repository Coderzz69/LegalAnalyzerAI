
# AutoLawyer - AI Legal Document Analysis

AutoLawyer is a Flask-based web application that uses AI to analyze legal documents, providing summaries and plain-English explanations of key clauses.

## Features

- Document upload and analysis
- AI-powered legal document interpretation
- Clause-by-clause breakdown
- Document history tracking
- Clean, modern UI with Bootstrap 5

## Tech Stack

- Python 3.x with Flask
- SQLAlchemy for database management
- OpenAI GPT-4 for document analysis
- Bootstrap 5 for frontend
- Gunicorn for production server

## Getting Started

1. Click the "Run" button in your Replit workspace
2. The application will start automatically on port 5000
3. Upload a legal document through the web interface
4. View the AI-generated analysis and explanations

## Project Structure

```
├── static/          # Static assets (CSS, JS)
├── templates/       # HTML templates
├── app.py          # Main Flask application
├── models.py       # Database models
├── utils.py        # Utility functions for AI analysis
└── main.py         # Application entry point
```

## API Routes

- `/` - Home page with document upload
- `/analyze` - Document analysis endpoint
- `/result` - Analysis results page
- `/history` - Document analysis history
- `/document/<id>` - View specific document analysis

## Database Schema

- Document table: Stores document metadata and analysis
- Clause table: Stores individual clause analysis results

## Environment Variables

Required environment variables:
- `DATABASE_URL`: Database connection string
- `SESSION_SECRET`: Secret key for session management
- `OPENAI_API_KEY`: OpenAI API key for analysis

## Deployment

The application is automatically deployed on Replit and accessible via the provided URL.
