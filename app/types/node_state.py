from typing import Annotated, List, Optional, Dict, Sequence
from pydantic import BaseModel, Field
from langgraph.graph.message import AnyMessage, add_messages

from app.types.jd_schema import JDSchema
from app.types.userdetails_schema import UserDetails

class NodeState(BaseModel):
    """
    Represents the state of a node in the processing graph.

    Attributes:
        messages (Sequence[AnyMessage]): Sequence of messages exchanged during node execution.
        intent (Optional[str]): Intent of the process, such as "resume" or "cover_letter".
        is_jd_given (bool): Indicates if a job description is provided.
        job_description (Optional[Union[str, JDSchema]]): Job description or its parsed schema.
        user_details (Optional[Dict]): Additional user details, if available.
        cover_letter (Optional[str]): Generated cover letter, if applicable.
    """
    messages: Annotated[Sequence[AnyMessage], add_messages]
    intent: Optional[str] = Field(default=None, required=False)
    is_jd_given: bool = Field(default=False)
    job_description: Optional[str | JDSchema] = Field(default="")
    user_details: Optional[Dict]
    cover_letter: Optional[str] = Field(required=False, default="")