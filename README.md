# 🧹 MAFIA Backend System

This project is a backend service for the MAFIA Web Application, built with **Flask**, **Python**, and **MySQL**, running in **Docker containers**. It includes structured layers for handling API, business logic, database interaction, and supports database migration with Alembic.

---

## 📁 Directory Structure

### Backend Server (`mafia_backend/`)

```text
mafia_backend/
├── app/                       # Main application logic
│   ├── adapters/             # Adapter layer (DB, models, repos, exceptions)
│   │   ├── database/         # DB session & connection setup (MySQL)
│   │   ├── models/           # ORM model classes
│   │   └── repositories/     # Repository implementations & interfaces
│   ├── container.py          # Dependency Injection setup
│   ├── dto/                  # Data Transfer Objects for JSON I/O
│   ├── presentations/        # Flask Blueprints (API layer)
│   ├── services/             # Business logic / use cases
│   ├── utils/                # Reusable utility functions (e.g., auth_utils.py)
│   ├── app_dev.py            # Application entrypoint and DI wiring
├── .env                      # Environment variables (DB connection, secrets)
├── Dockerfile                # Docker build config for backend service
├── requirements.txt          # Python package dependencies
├── test/                     # Unit & integration tests
└── docker-compose.yaml       # Docker orchestration file
```

---

## 🛠 Backend Installation Guide

### 1) Place Source Code on Server

Place the backend source code under a directory named `mafia_backend`.

### 2) Build and Launch Backend Container

```bash
cd mafia_backend
docker-compose up -d --build
```

### 3) Verify Running Containers

```bash
docker ps
```

Ensure that the backend container is running correctly.

---

## 🛩 Backend Architecture Overview

The system follows a layered architecture:

- **Presentation Layer**: HTTP interface using Flask, defines endpoints and routes.
- **Service Layer**: Contains business logic (e.g., tax calculation, fund management).
- **Adapter Layer**: Bridges the system with external interfaces and databases.
  - **Repository**: Handles data access via MySQL.
  - **Model**: ORM mapping to MySQL tables.
  - **Database**: Configures DB engine and sessions.
- **Dependency Injection**: Managed via `container.py`.
- **Authentication**: Handled via JWT and security headers (e.g., Talisman).

---

## 🔄 Database Migration System (`mafia-migrations/`)

```text
mafia-migrations/
├── app/
│   ├── data/                 # Seed data for initial load
│   ├── migrations/           # Alembic migration scripts and env.py
│   │   └── versions/         # Auto-generated version scripts
│   ├── models/               # DB models for Alembic autogenerate
│   └── ...                   # Configs and helpers
├── .env                      # Database credentials
├── Dockerfile                # Docker build for migration service
├── alembic.ini               # Alembic configuration
├── entrypoint.sh             # Init script for container
├── requirements.txt          # Python dependencies
└── docker-compose.yaml       # Docker orchestration for DB service
```

---

## 🛠 Database Installation Guide

### 1) Place Source Code on Server

Place the database migration project under a folder named `mafia-migrations`.

### 2) Create Docker Network

```bash
docker network create shared_network
```

### 3) Build and Launch Database Container

```bash
cd mafia-migrations
docker-compose up -d --build
```

### 4) Verify Container Status

```bash
docker ps
```

Ensure the MySQL database container is running and accessible.

---

## 🔀 Database Migration with Alembic

- Models in `models/` are used to generate schema.
- Run migration with:

```bash
alembic revision --autogenerate -m "<message>"
alembic upgrade head
```

---

## ✅ Notes

- The `.env` files in both `mafia_backend` and `mafia-migrations` must match for consistent DB connection.
- Required keys to be configured in both `.env` files:

```env
MYSQL_ROOT_PASSWORD=
MYSQL_DATABASE=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_URL=
JWT_SECRET_KEY=
```

- All services run in isolated containers but communicate over a shared Docker network.
- Use `entrypoint.sh` to initialize data if needed.

---

## 🛠 Tech Stack

- Python 3.x
- Flask
- SQLAlchemy
- Alembic (for migrations)
- MySQL
- Docker / Docker Compose

---


