from typing import Annotated, List, Optional, Dict
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages

from app.types.jd_schema import JDSchema
from app.types.userdetails_schema import UserDetails

class NodeState(BaseModel):
    user_query: str = Field(required=True)
    intent: Optional[str] = Field(default=None, required=False)
    is_jd_given: bool = Field(default=False)
    job_description: Optional[str | JDSchema] = Field(default="")
    user_details: Optional[Dict]


