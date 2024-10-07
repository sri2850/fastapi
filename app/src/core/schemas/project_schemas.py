from typing import Optional

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    description: str
    # owner_id: int = Optional

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass