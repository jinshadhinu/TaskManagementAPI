from fastapi import FastAPI
from database import create_table
from routes.task_routes import router as task_router

app=FastAPI(
    title="Task Management API",
    description="A REST API to create, manage, filter, and tracks using SQLite",
    version="1.0.0"
)
 #create database table
create_table()

#register task routes
app.include_router(task_router)

@app.get("/")
def home():
 return {
  "message":" Welcome to Task management API"
 }