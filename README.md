# technical-test-backend
![Python](https://img.shields.io/badge/Python-grey?logo=python)

Technical test for Backend Role
---

## 📑 Table of Contents

- [Quick Start](#-quick-start)
- [Architecture Overview](#-architecture-overview)
- [Local Development](#-local-development)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [Environment Variables](#-environment-variables)
- [Tech Stack](#-tech-stack)
- [Project Metadata](#-project-metadata)
- [Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Start

### Prerequisites

- [Python](https://www.python.org/) + [uv](https://docs.astral.sh/uv/)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/avahi-org/technical-test-backend.git
   cd technical-test-backend
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env
   # Fill in your values
   ```

4. **Run locally**
   ```bash
   uv run python main.py
   ```

---

## 🏗 Architecture Overview

<!-- Describe the system architecture and add a diagram if applicable -->

### Core Components

| Component | Description |
|-----------|-------------|
| <!-- Component --> | <!-- Description --> |

---

## 💻 Local Development

### Without Docker

```bash
uv sync
uv run python main.py
```

### With Docker

```bash
# Build
docker build -t technical-test-backend:dev .

# Run
docker run -it --rm -p 8080:8080 --env-file .env technical-test-backend:dev
```

---

## 🚢 Deployment

<!-- Deployments are typically automated via GitHub Actions on push to develop. -->

### Deploy to Development

```bash
git push origin develop
```

---

## 🗂 Project Structure

```
technical-test-backend/
├── .github/
│   └── workflows/       # CI/CD pipelines
├── src/                 # Application source code
├── main.py              # Entry point
├── Dockerfile           # Production container
├── pyproject.toml       # Dependencies
└── README.md
```

---

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| <!-- VAR_NAME --> | ✅ | <!-- Description --> |

> ⚠️ Never commit `.env` files — they are gitignored by default.

---

## 📦 Tech Stack

| Component | Description |
|-----------|-------------|
| Python | Application logic and scripting |

---

## 📋 Project Metadata

**Project Type:** Internal Infra

### Team

| Role | GitHub Username |
|------|----------------|
| Lead | @OscarAvahi |

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| <!-- Issue --> | <!-- Solution --> |
