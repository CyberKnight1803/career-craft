from typing import List
from pydantic import BaseModel, Field

class RatingSchema(BaseModel):
    """
    Schema for storing rating information provided by an expert judge.

    Attributes:
        rating (int): Rating score, default is 5, valid range is 1 to 5.
    """
    rating: int = Field(description="Rating given by the expert judge.", default=5)

class SkillsSchema(BaseModel):
    """
    Schema for storing a list of skills extracted from the job description.

    Attributes:
        skills (List[str]): List of skills.
    """
    skills: List[str] = Field(description="List of skills extracted from the job description.", default=[])