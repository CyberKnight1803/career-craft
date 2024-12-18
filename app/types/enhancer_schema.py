from typing import List 
from pydantic import BaseModel, Field


class EnhancerSchema(BaseModel):
    """
    Schema for storing enhanced points or descriptions.

    Attributes:
        enhanced_points (List[str]): List of enhanced and improved descriptions.
    """
    enhanced_points: List[str] = Field(description="Enhanced and improved list of descriptions")