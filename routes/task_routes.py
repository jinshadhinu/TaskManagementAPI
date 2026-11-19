from fastapi import APIRouter, HTTPException, status
from schemas.task_schema import(
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    TaskResponse
)
from services.task_service import(
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    update_task_status,
    delete_task
)

router =APIRouter(prefix="/tasks",tags=["Tasks"])

# get all tasks+filtering
@router.get("/",response_model=list[TaskResponse])
def read_tasks(
    status_filter :str |None =None,
    priority :str |None =None
):
    valid_statuses=[
        "Pending","In Progress","Completed"
    ]
    valid_priorities=[
         "Low",
        "Medium",
        "High"
    ]

    if status_filter is not None and status_filter not in valid_statuses:
        raise HTTPException(status_code=400,
                            detail ="Invalid task status"
                            )
    if priority is not None and priority not in valid_priorities:
        raise HTTPException(
            status_code=400,detail="Invalid task priority "
        )
    return get_all_tasks(
        status=status_filter,priority=priority
    )

# get task by id
@router.get("/{task_id}",response_model=TaskResponse)
def read_task(task_id: int):
    return get_task_by_id(task_id)

#create task
@router.post("/",response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def add_task(task: TaskCreate):
    return create_task(task.model_dump())

#update task details
@router.put("/{task_id}",response_model=TaskResponse)
def edit_task(task_id: int, task:TaskUpdate):
    update_data= task.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Please provide atleast one field to update"
        )
    if any(value is None for value in update_data.values()):
        raise HTTPException(
            status_code=400,
            detail="Task fields cannot be null"
        )
    return update_task(task_id,update_data)

#update task status
@router.patch("/{task_is}/status",response_model=TaskResponse)
def edit_task_status(task_id: int, task:TaskStatusUpdate):
    return update_task_status(task_id,task.status)

#delete task
@router.delete("/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
def remove_task(task_id: int):
    delete_task(task_id)
    return None
