from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.integration import CalendarProfile, Task
from app.schemas.integration import Task as TaskSchema, CreateTask, UpdateTask
from app.api.auth import get_current_user
from app.db.session import get_db
from app.core.auth import auth_responses

task_router = APIRouter(
    responses=auth_responses,
)


@task_router.get("", response_model=list[TaskSchema], operation_id="list_tasks")
async def list_tasks(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve all tasks for the current user."""

    tasks = (
        db.query(Task)
        .join(Task.profile)
        .filter(Task.profile.has(user_id=user.id))
        .all()
    )

    return tasks


@task_router.post(
    "", response_model=TaskSchema, status_code=201, operation_id="create_task"
)
async def create_task(
    task_data: CreateTask,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new task for the current user."""

    profile = None
    if task_data.profile_id:
        profile = (
            db.query(CalendarProfile)
            .filter(
                CalendarProfile.id == task_data.profile_id,
                CalendarProfile.user_id == user.id,
            )
            .first()
        )
        if not profile:
            raise HTTPException(status_code=404, detail="Calendar profile not found")

    task = Task(
        title=task_data.title,
        description=task_data.description,
        due_date=task_data.due_date,
        duration=task_data.duration,
        priority=task_data.priority,
        not_before=task_data.not_before,
        profile=profile,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@task_router.delete("/{task_id}", status_code=204, operation_id="delete_task")
async def delete_task(
    task_id: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a task by ID."""

    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.profile.has(user_id=user.id))
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()


@task_router.get("/{task_id}", response_model=TaskSchema, operation_id="get_task")
async def get_task(
    task_id: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve a task by ID."""

    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.profile.has(user_id=user.id))
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@task_router.put("/{task_id}", response_model=TaskSchema, operation_id="update_task")
async def update_task(
    task_id: str,
    task_data: UpdateTask,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a task by ID."""

    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.profile.has(user_id=user.id))
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_data.completed is not None:
        task.completed = task_data.completed
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    if task_data.duration is not None:
        task.duration = task_data.duration
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.not_before is not None:
        task.not_before = task_data.not_before

    db.commit()
    db.refresh(task)

    return task
