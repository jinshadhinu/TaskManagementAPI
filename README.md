
# Task Management API

A RESTful Task Management API built using Python, FastAPI and SQLite.

## Features

- Create tasks
- Retrieve all tasks
- Retrieve task by ID
- Update task details
- Update task status
- Delete tasks
- Filter tasks by status
- Filter tasks by priority
- Input validation using Pydantic
- SQLite database integration
- Automated endpoint testing using Pytest

## Technologies Used

- Python
- FastAPI
- SQLite
- Pydantic
- Pytest
- Uvicorn

## Project Structure

```text
TaskManagementAPI/
├── main.py
├── database.py
├── schemas/
├── routes/
├── services/
├── tests/
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project:

```bash
cd TaskManagementAPI
```

Create a virtual environment:

```bash
python -m venv myvenv
```

Activate the environment on Windows:

```bash
myvenv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the application

```bash
uvicorn main:app --reload
```

## API Documentation

Open:

http://127.0.0.1:8000/docs

## Run tests

```bash
python -m pytest -v
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /tasks/ | Create task |
| GET | /tasks/ | Get all tasks |
| GET | /tasks/{task_id} | Get task by ID |
| PUT | /tasks/{task_id} | Update task |
| PATCH | /tasks/{task_id}/status | Update status |
| DELETE | /tasks/{task_id} | Delete task |

## Filtering

Filter by status:

```text
GET /tasks/?status_filter=Pending
```

Filter by priority:

```text
GET /tasks/?priority=High
```

## Database

SQLite is used to store task records persistently.

## Author

Jinsha Dhinu