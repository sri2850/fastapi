
from fastapi import APIRouter
from sqlalchemy import select
from starlette import status
from starlette.exceptions import HTTPException

from app.src.core.models.models import Project, Task
from app.src.core.routers.user import db_dependency

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks Data"]
)

@router.get("/{project_name}", status_code=status.HTTP_200_OK)
async def get_tasks_for_project(project_name: str, db: db_dependency):
    # project = (await db.execute(select(Project).where(Project.name == project_name))).scalar()
    # if not project:
    #     raise HTTPException(status_code=404, detail='project not found')
    # result = await db.execute(select(Task).where(Task.title == project_name))
    # tasks = result.scalars().all()
    # if not tasks:
    #     raise HTTPException(status_code=404, detail='tasks not found')
    # return tasks

    # using Joins
    query = (
        select(Task)
        .join(Project, Task.project_id == Project.id)
        .where(Project.name == project_name)
    )

    # Execute the query
    result = await db.execute(query)
    tasks = result.scalars().all()

    # Check if tasks are found
    if not tasks:
        raise HTTPException(status_code=404, detail='No tasks found for this project')

    return tasks