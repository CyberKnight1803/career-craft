from typing import List 
from pydantic import BaseModel, Field


class JDSchema(BaseModel):
    """
    Schema for storing job description details.

    Attributes:
        position (str): Job title or position.
        organization (str): Organization name.
        responsibilities (List[str]): List of summarized responsibilities.
        skills (List[str]): List of skills required for the job.
    """
    position: str = Field(description="Job Title")
    organization: str = Field(description="Organization")
    responsibilities: List[str] = Field(description="Summarized Responsibilities")
    skills: List[str]