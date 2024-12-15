from typing import List
from pydantic import BaseModel, Field

class RatingSchema(BaseModel):
    rating: int = Field(description="Rating given by the expert judge.", default=5)

class SkillsSchema(BaseModel):
    skills: List[str] = Field(description="List of skills extracted from the job description.", default=[])