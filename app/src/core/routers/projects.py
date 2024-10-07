from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from scripts.regsetup import description
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from app.src.common.config.database import SessionLocal
from app.src.core.models.models import Project, Task
from app.src.core.schemas.project_schemas import ProjectCreate, ProjectUpdate
from app.src.core.schemas.task_schemas import TaskCreate

router = APIRouter(
    prefix="/projects",
    tags=["Project Data"]
)

async def get_db():
    async with SessionLocal() as session:
        yield session

db_dependency = Annotated[AsyncSession, Depends(get_db)]

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_projects(db: db_dependency):
    result = await db.execute(select(Project))
    return result.scalars().all()

@router.put("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_project_details(project_id: int, project_details: ProjectUpdate, db: db_dependency):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar()
    if project is None:
        raise HTTPException(status_code=401, detail='project details not found')

    project.name = project_details.name
    project.description = project_details.description
    # Project.owner_id = project_details.owner_id
    await db.commit()
    await db.refresh(project)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, db: db_dependency):
    project = (await db.execute(select(Project).where(Project.id == project_id))).scalar()
    if not project:
        raise HTTPException(status_code=401, detail='project details not found')
    await db.delete(project)
    await db.commit()

@router.post("/{project_id}/tasks", status_code=status.HTTP_201_CREATED)
async def create_task_for_project(project_id: int, task: TaskCreate, db: db_dependency):
    project = (await db.execute(select(Project).where(Project.id == project_id))).scalar()
    if not project:
        raise HTTPException(status_code=401, detail='project details not found')
    new_task = Task(
        title = task.title,
        description = task.description,
        status = task.description,
        assignee_id = project.owner_id,
        project_id = project_id
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

