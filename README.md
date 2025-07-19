# AIlthy BillClear MVP

Simplify confusing medical bills in seconds using the power of OpenAI.  
This MVP ships as a single‑command Docker deployment so that anyone—technical or not—can try it locally.

⸻

## ✨ Key Features

| What you get              | Why it matters                                                     |
| ------------------------- | ------------------------------------------------------------------ |
| **AI bill explainer**     | Paste any medical bill text and receive a jargon‑free explanation. |
| **Email + phone capture** | Optionally collect contact details for follow‑up or analytics.     |
| **Zero‑install backend**  | Everything (FastAPI, PostgreSQL, Alembic) runs inside Docker.      |
| **Interactive web UI**    | Clean HTML/CSS/JS front page at localhost:8000.                    |
| **Self‑documenting API**  | Full Swagger docs at localhost:8000/docs.                          |

## 🧰 Prerequisites

1. **Docker Desktop**
   • Download & install from https://www.docker.com/ (Windows / macOS / Linux).  
   • Make sure it is running before you continue.

## 🚀 Quick‑Start

```bash
# 1 — clone the repo
git clone git@github.com:iProgrammerDmytro/AIlthy-Bill-Clear.git
cd AIlthy-Bill-Clear

# 2 — create .env file and add your OpenAI API key
cp .env.example .env
# Edit .env file and paste your OPENAI_API_KEY

# 3 — first time: build & start everything
docker compose up --build

# 4 — run database migrations (necessary step)
docker compose exec api alembic upgrade head

# 5 — next times: just start
docker compose up
```

**Tip:** Press Ctrl + C once to stop the stack, or run `docker compose down` to stop and remove containers.

## 🌐 Using the App

1. Open http://localhost:8000 in your browser.
2. Paste the raw text of a medical bill.
3. Enter an email (required) and phone (optional).
4. Click "Simplify".
5. Read the AI‑generated, plain‑English explanation.

## 📁 Project Structure

```
app/
├── bill/            # Bill‑related routes, services, tests
├── contact/         # Email & phone capture logic
├── core/            # OpenAI client, settings, prompts
├── db/              # SQLAlchemy database session + Alembic
├── static/          # style.css, script.js
└── templates/       # index.html
docker-compose.yml   # runs API + PostgreSQL
Dockerfile           # Python 3.12, pip‑install, uvicorn
requirements.txt     # production deps
requirements.dev.txt # dev + test deps (pytest, etc.)
```
