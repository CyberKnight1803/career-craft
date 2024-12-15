from typing import Literal
from langchain_core.runnables import RunnableConfig
from langgraph.types import interrupt, Command

from app.types.node_state import NodeState

def handle_doc_type(state: NodeState, config: RunnableConfig) -> Literal["resume_rephraser", "cover_letter_rephraser"]:
    if state.intent == "resume": 
        return "resume_rephraser" 

    elif state.intent == "cover_letter":
        return "cover_letter_rephraser"