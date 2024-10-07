from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status
from starlette.exceptions import HTTPException
from app.src.common.config.database import SessionLocal
from app.src.core.models.models import Users, Project
from app.src.core.schemas.project_schemas import ProjectCreate
from app.src.core.schemas.user_schemas import UserCreate

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


db_dependency = Annotated[AsyncSession, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: UserCreate, db: db_dependency):
    async with db.begin():
        # new_user = Users(**create_user_request.model_dump(), owner_id=create_user_request.get('id'))
        new_user = Users(
            username=create_user_request.username,
            email=create_user_request.email,
            full_name=create_user_request.full_name,
            is_active=create_user_request.is_active
        )
        db.add(new_user)
        await db.commit()
        # await db.refresh(new_user)
        return new_user

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency):
    result = await db.execute(select(Users))
    return result.scalars().all()

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db: db_dependency):
    result = await db.execute(select(Users).where(Users.id == user_id))
    user = result.scalars().first()
    return user

@router.post("/{user_id}/project", status_code=status.HTTP_201_CREATED)
async def create_project_for_user(user_id: int, project: ProjectCreate, db: db_dependency):
    result = await db.execute(select(Users).where(Users.id == user_id))
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
    new_project = Project(
        name = project.name,
        description = project.description,
        owner_id = user_id
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project
