
# 🌌 Planetary API

A simple RESTful Flask API for managing planetary data in our solar system. Built with Flask, SQLAlchemy, and JWT authentication.

## 🚀 Features

- Add, list, and query planets
- User login with JWT authentication
- SQLite as a lightweight database
- CLI commands for database management
- Modular code structure (`models`, `routes`, `commands`)

---

## 📁 Project Structure

```
planetary-api/
│
├── app.py                  # Flask app setup
├── models.py               # Database models and schemas
├── routes.py               # API route handlers
├── commands.py             # Custom CLI commands (db_create, db_seed, etc.)
├── planets.db              # SQLite database (auto-generated)
├── requirements.txt        # Python dependencies
└── ...
```

---

## 🛠️ Installation

1. **Clone the repo** and **create a virtual environment**:

```bash
git clone <repo-url>
cd planetary-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Initialize the database**:

```bash
flask db_create
flask db_seed
```

---

## 🔐 Authentication

This API uses JWT (JSON Web Tokens) for securing some routes. Obtain a token by logging in:

### Login

```http
POST /login
Content-Type: application/json

{
  "email": "test@test.com",
  "password": "P@ssw0rd"
}
```


---

## 📡 API Endpoints

| Method | Endpoint                  | Description                  | Auth Required |
|--------|---------------------------|------------------------------|----------------|


| GET    | `/parameters?name=...`    | Query example                | ❌             |
| GET    | `/url_variables/<name>/<age>` | URL param example         | ❌             |
| GET    | `/planets`                | List all planets             | ❌             |
| POST   | `/add_planet`             | Add a new planet             | ✅ JWT         |
| POST   | `/login`                  | User login (get token)       | ❌             |





