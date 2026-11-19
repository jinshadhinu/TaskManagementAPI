from fastapi import HTTPException
from database import get_connection
import sqlite3

#get all tasks
def get_all_tasks(status=None, priority= None):
    query= "SELECT * FROM tasks WHERE 1=1"
    values =[]
    if status is not None:
        query+= " AND status= ?"
        values.append(status)
    if priority is not None:
        query +=" AND priority =?"
        values.append(priority)

    query += " ORDER BY id"

    with get_connection() as connection :
        cursor=connection.execute(query,values)
        tasks= cursor.fetchall()
        return [dict(task) for task in tasks]


# get task by id
def get_task_by_id(task_id:int):
    with get_connection() as connection:
        cursor= connection.execute(
            "SELECT * FROM tasks WHERE id= ?",(task_id,)
        )
        task= cursor.fetchone()
        if task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return dict(task)

# create task
def create_task(task_data :dict):
    try:
        with get_connection() as connection:

            cursor = connection.execute(
                """
                INSERT INTO tasks
                (title, description, priority, status)
                VALUES (?, ?, ?, ?)
                """,
                (
                    task_data["title"],
                    task_data["description"],
                    task_data["priority"],
                    task_data["status"]
                )
            )

            new_id = cursor.lastrowid

            new_task = connection.execute(
                "SELECT * FROM tasks WHERE id = ?",
                (new_id,)
            ).fetchone()

            return dict(new_task)

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Task could not be created due to a database constraint"
        )

#update task

def update_task(task_id: int , update_data: dict):
    get_task_by_id(task_id)
    allowed_fields={
        "title","description","priority","status"
    }
    fields=[field for field in update_data
            if field in allowed_fields
            ]
    if not fields:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )
    set_clause=",".join(
        f"{field}= ?" for field in fields
    )
    values =[update_data[field] for field in fields]
    values.append(task_id)
    with get_connection() as connection:
        connection.execute(
            f" UPDATE tasks SET {set_clause} where id=?",values
        )
        updated_task = connection.execute(
            "SELECT * FROM tasks WHERE id= ?",(task_id,)
        ).fetchone()

        return dict(updated_task)

#update task status 

def update_task_status(task_id: int, status:str):
    get_task_by_id(task_id)

    with get_connection() as connection :
        connection.execute("UPDATE tasks SET status= ? WHERE id= ?",
                           (status,task_id))
        updated_task = connection.execute(
                    "SELECT * FROM tasks WHERE id= ?",(task_id,)
                ).fetchone()
        
        return dict(updated_task)

#delete task

def delete_task(task_id: int):
    get_task_by_id(task_id)

    with get_connection() as connection:
        connection.execute(
            "DELETE FROM tasks WHERE id= ?",
            (task_id,)
        )
    return None
 