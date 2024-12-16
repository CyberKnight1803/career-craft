from typing import List 
from pydantic import BaseModel, Field


class EnhancerSchema(BaseModel):
    enhanced_points: List[str] = Field(description="Enhanced and improved list of descriptions")