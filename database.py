import sqlite3
from pathlib import Path
from contextlib import contextmanager

DATABASE_PATH =Path(__file__).resolve().parent/"tasks.db"

@contextmanager
def get_connection():
    connection =sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

def create_table():
    with get_connection() as connection:
        connection.execute("""
        create table if not exists tasks(
        id integer primary key autoincrement,
        title text not null,uv
        description text,
        priority text not null check(priority in('Low','Medium','High')),
        status text not null default 'Pending' check (status in ('Pending','In Progress','Completed'))
        )""")
