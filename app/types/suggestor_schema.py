from typing import List, Dict
from pydantic import BaseModel, Field


class SuggestorSchema(BaseModel):
    experiences: List[Dict] = Field(description="Relevant Experiences", default=[])
    projects: List[Dict] = Field(description="Relevant Projects", default=[])
    skills: List[str] = Field(description="Relevant Skills", default=[])