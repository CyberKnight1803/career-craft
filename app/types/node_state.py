from typing import Annotated, List, Optional, Dict, Sequence
from pydantic import BaseModel, Field
from langgraph.graph.message import AnyMessage, add_messages

from app.types.jd_schema import JDSchema
from app.types.userdetails_schema import UserDetails

class NodeState(BaseModel):
    messages: Annotated[Sequence[AnyMessage], add_messages]
    # user_query: str = Field(required=True)
    intent: Optional[str] = Field(default=None, required=False)
    is_jd_given: bool = Field(default=False)
    job_description: Optional[str | JDSchema] = Field(default="")
    user_details: Optional[Dict]

    cover_letter: Optional[str] = Field(required=False, default="")



