import sqlite3
import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_connection

client=TestClient(app)

@pytest.fixture(autouse=True)
def reset_database():
    with get_connection() as connection:
        connection.execute("Delete from tasks")

        #reset the sqlite to id counter
        connection.execute("Delete from sqlite_sequence where name= 'tasks'")
        yield

def sample_task():
    return{
        "title":  "Complete FastAPI project",
        "description": "Build Task Management API",
        "priority": "High",
        "status": "Pending"
    }

#test home
def test_home():
    response=client.get("/")
    assert response.status_code ==200

#test create task
def test_create_task():
    response= client.post("/tasks/",
                          json= sample_task())
    assert response.status_code ==201
    assert response.json()["title"] =="Complete FastAPI project"


#test get all tasks
def test_get_all_tasks():
    response= client.get("/tasks/")
    assert response.status_code ==200
    assert len(response.json()) ==1

#test get task by ud
def test_get_task_by_id():
    created = client.post("/tasks/",
                          json=sample_task())
    task_id= created.json()["id"]
    response =client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] ==task_id

# TEST NONEXISTENT TASK
def test_task_not_found():
    response =client.get("/tasks/999")
    assert response.status_code ==404

# TEST UPDATE TASK
def test_update_status():
    created=client.post("/tasks/",json=sample_task())
    task_id= created.json()["id"]
    response =client.patch(
        f"/tasks/{task_id}/status",
        json ={"status":"Completed"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "Completed"

# TEST DELETE TASK
def test_delete_task():
    created =client.post(
        "/tasks/",json=sample_task()
    )
    task_id=created.json()["id"]
    response= client.delete(f"/tasks/{task_id}")
    assert response.status_code ==204
    check = client.get(f"/tasks/{task_id}")
    assert check.status_code ==404
