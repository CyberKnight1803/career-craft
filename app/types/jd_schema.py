from typing import List 
from pydantic import BaseModel, Field


class JDSchema(BaseModel):
    position: str = Field(description="Job Title")
    organization: str = Field(description="Organization")
    responsibilities: List[str] = Field(description="Summarized Responsibilities")
    skills: List[str]