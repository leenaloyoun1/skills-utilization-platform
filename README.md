# Skills Utilization Platform & Course Recommendation Engine

An AI-powered course recommendation platform that helps users discover relevant learning opportunities based on their skills and learning interests.

The project combines:

- OpenAI-based skill extraction
- Semantic embeddings
- Similarity-based recommendations
- PostgreSQL database integration
- Flask web application
- LangGraph workflow orchestration
- AI agents, guardrails, and fallback logic

---

# Features

## Recommendation Engine

- Extract skills from free-form user text
- Generate semantic embeddings
- Build user profile vectors using average pooling
- Compare users and courses using cosine similarity
- Rank courses by relevance
- Return Top-N recommendations

## Database Integration

- PostgreSQL database
- SQLAlchemy Core
- Users, Skills, Courses, UserSkills
- Embeddings storage
- Recommendation logs

## AI & Workflow Features

- Skill Extraction Agent
- Validation Agent
- Recommendation Agent
- Fallback Agent
- Logging Agent
- LangGraph workflow orchestration
- Guardrails and validation
- Default recommendations for unsupported inputs

## Interfaces

### Flask Web Application

```text
http://127.0.0.1:5000
```

Users can:

- Enter learning interests
- Request recommendations
- View extracted skills
- View recommended courses

### REST API

```http
POST /api/recommend
```

Supports:

- Recommendation by user ID
- Recommendation by free-form text

### Command Line Interface

```bash
python cli.py
```

Interactive menu:

```text
1. Recommend by User ID
2. Recommend by Text
3. Exit
```

---

# Technology Stack

## Backend

- Python 3.14
- Flask
- SQLAlchemy Core
- PostgreSQL
- Psycopg

## AI & Machine Learning

- OpenAI
- Sentence Transformers
- NumPy
- Scikit-Learn

## Workflow & Agents

- LangChain
- LangGraph

## Testing

- Pytest

---

# Architecture

## Recommendation Pipeline

```text
User Input
    ↓
Skill Extraction
    ↓
Embedding Generation
    ↓
User Profile Vector
    ↓
Cosine Similarity
    ↓
Course Ranking
    ↓
Recommendations
```

---

## Day 3 Workflow

```text
START
  ↓
Skill Extraction Agent
  ↓
Validation Agent
  ↓
Valid Skills?
 /         \
Yes         No
 |           |
 ↓           ↓
Recommendation Agent
             Fallback Agent
        \   /
         ↓
     Logging Agent
         ↓
        END
```

---

# Database Schema

The project uses SQLAlchemy Core.

Tables:

- users
- skills
- courses
- user_skills
- embeddings
- recommendation_logs

---

# Project Structure

```text
project_5/
│
├── app/
│   ├── agents/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── repositories/
│   ├── services/
│   ├── static/
│   ├── templates/
│   ├── workflows/
│   └── flask_app.py
│
├── data/
├── scripts/
├── tests/
│
├── cli.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

# Setup Instructions

## 1. Clone the Repository

```bash
git clone <repository-url>
cd project_5
```

## 2. Create Virtual Environment

```bash
python3 -m venv .venv
```

## 3. Activate Environment

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Configure Environment Variables

Create:

```bash
cp .env.example .env
```

Update:

```env
OPENAI_API_KEY=your_key_here
DATABASE_URL=your_database_url
```

---

# Database Initialization

Create tables:

```bash
python -m scripts.create_database
```

Seed sample data:

```bash
python -m scripts.seed_database
```

Generate embeddings:

```bash
python -m scripts.seed_embeddings
```

---

# Running the Application

## Flask Web Application

```bash
flask --app app.flask_app run --debug
```

Open:

```text
http://127.0.0.1:5000
```

---

## Command-Line Interface

```bash
python cli.py
```

---

# API Usage

## Recommendation by User ID

Request:

```json
{
  "user_id": 1,
  "top_n": 3
}
```

---

## Recommendation by Text

Request:

```json
{
  "text": "I want to learn machine learning and NLP",
  "top_n": 3
}
```

---

## Example Response

```json
{
  "extracted_skills": [
    "Machine Learning",
    "Natural Language Processing"
  ],
  "recommended_courses": [
    {
      "title": "Natural Language Processing",
      "similarity_score": 0.89
    }
  ]
}
```

---

# Testing

Run all tests:

```bash
pytest
```

Run selected tests:

```bash
python -m tests.test_workflow
python -m tests.test_complete_workflow
python -m tests.test_database_recommendations
```

---

# Security

- API keys are stored in `.env`
- `.env` is excluded from Git
- `.env.example` contains placeholders only
- No secrets should be committed to source control

---

# Project Deliverables

✅ Embedding generation

✅ Recommendation engine

✅ PostgreSQL schema

✅ SQLAlchemy Core integration

✅ REST API

✅ Flask web application

✅ AI agents

✅ LangGraph workflow

✅ Guardrails

✅ Fallback recommendations

✅ Recommendation logging

✅ Automated testing

---

# License

This project was developed as part of the Practical Training Program and is intended for educational purposes.