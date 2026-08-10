# Skills Utilization Platform and Course Recommendation Engine

An AI-powered course recommendation platform that recommends relevant courses based on a user's skills and learning interests.

## Project Goal

The project builds a recommendation pipeline that:

1. Extracts skills from user input.
2. Converts skills and course descriptions into embeddings.
3. Creates a user-profile vector from the user's skill embeddings.
4. Compares the user vector with course vectors using cosine similarity.
5. Ranks courses and returns the Top N recommendations.
6. Provides similarity scores and explanations for the results.

## Core Features

- Skill extraction from text or predefined input
- Skill embedding generation
- Course-description embedding generation
- User-profile vector creation using average pooling
- Semantic course matching using cosine similarity
- Top N course recommendations
- FastAPI endpoint at `POST /api/recommend`
- Relational database integration using SQLAlchemy Core
- Recommendation logging
- Guardrails and fallback recommendations
- LangChain tools and LangGraph workflow orchestration

## Technology Stack

- Python 3.14
- FastAPI
- Uvicorn
- SQLAlchemy Core
- SQLite
- Sentence Transformers
- NumPy
- scikit-learn
- LangChain and LangGraph, added during the workflow stage
- pytest

## Database Approach

This project uses SQLAlchemy Core only.

The database layer will use:

- `Engine`
- `Connection`
- `MetaData`
- `Table`
- `Column`
- `select()`
- `insert()`
- `update()`
- `delete()`

The project does not use SQLAlchemy ORM models or ORM sessions.

## Database Tables

The database will contain:

- `users`
- `skills`
- `courses`
- `user_skills`
- `embeddings`
- `recommendation_logs`

## Project Structure

```text
project_5/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── repositories/
│   ├── services/
│   └── workflows/
├── data/
├── scripts/
├── tests/
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd project_5
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

On Linux or macOS:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure environment variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Add private API credentials to `.env` when required.

Never commit `.env` or API keys to Git.

## Environment Variables

```env
APP_NAME="Skills Utilization Platform"
APP_ENV=development
DEBUG=true

DATABASE_URL=sqlite:///./skills_platform.db

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
DEFAULT_TOP_N=3

OPENAI_API_KEY=
LOG_LEVEL=INFO
```

## Recommendation Process

The recommendation pipeline will:

1. Receive a user ID or user text.
2. Extract or retrieve the user's skills.
3. Generate an embedding for every skill.
4. Average the skill embeddings into a user-profile vector.
5. Retrieve course embeddings.
6. Calculate cosine similarity between the user and each course.
7. Rank courses from highest to lowest similarity.
8. Return the Top N courses with scores and explanations.
9. Record the recommendation result in the database.

## API Endpoint

```http
POST /api/recommend
```

Example request using a user ID:

```json
{
  "user_id": 1,
  "top_n": 3
}
```

Example request using text:

```json
{
  "text": "I want to learn artificial intelligence and backend development",
  "top_n": 3
}
```

Planned response format:

```json
{
  "user_id": 1,
  "extracted_skills": [
    "Artificial Intelligence",
    "Backend Development"
  ],
  "recommended_courses": [
    {
      "course_id": 1,
      "title": "Machine Learning Foundations",
      "similarity_score": 0.91,
      "explanation": "This course closely matches the user's artificial intelligence interests."
    }
  ]
}
```

## Testing

Tests will cover:

- Skill extraction
- Embedding generation
- User-profile vector creation
- Cosine-similarity ranking
- Database queries
- API requests and responses
- Guardrails and fallback behavior

Run tests with:

```bash
pytest
```

## Development Plan

### Day 1: Core AI Engine

- Skill extraction
- Embedding generation
- Average pooling
- Cosine similarity
- Top N recommendation function

### Day 2: Backend Integration

- SQLAlchemy Core schema
- Sample users, skills, and courses
- Database-connected recommendation pipeline
- FastAPI recommendation endpoint
- Testing and validation

### Day 3: Advanced Extension

- LangChain tools and agents
- LangGraph workflow orchestration
- Guardrails
- Fallback recommendations
- Recommendation logging

## Security

- API keys are stored only in `.env`.
- `.env` is excluded from Git.
- `.env.example` contains placeholders only.
- API keys must never be written in source code, screenshots, commits, or documentation.

## Project Status

Day 1 core recommendation engine complete.

Implemented:
- OpenAI-based skill extraction
- Predefined skill-extraction fallback
- Skill and course embeddings
- Average-pooled user-profile vectors
- Cosine-similarity ranking
- Top N recommendations
- Similarity scores and recommendation explanations