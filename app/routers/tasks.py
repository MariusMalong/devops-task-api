from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=List[schemas.TaskOut])
def get_tasks(
    priority: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    query = db.query(models.Task).filter(models.Task.owner_id == current_user.id)
    if priority:
        query = query.filter(models.Task.priority == priority)
    return query.all()


@router.post("/", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_task = models.Task(**task.model_dump(), owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id, models.Task.owner_id == current_user.id
    ).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id, models.Task.owner_id == current_user.id
    ).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()
    return None