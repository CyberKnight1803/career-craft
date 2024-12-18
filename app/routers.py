from typing import Literal
from langchain_core.runnables import RunnableConfig
from langgraph.types import interrupt, Command

from app.types.node_state import NodeState

def handle_doc_type(state: NodeState, config: RunnableConfig) -> Literal["resume_rephraser", "cover_letter_rephraser"]:
    if state.intent == "resume": 
        return "resume_rephraser" 

    elif state.intent == "cover_letter":
        return "cover_letter_rephraser"
    

def handle_missing_info(state: NodeState, config: RunnableConfig) -> Literal["get_missing_jd", "get_missing_intent", "jd_analysis"]:
    if state.is_jd_given and (state.intent != "" and state.intent is not None):
        return "jd_analysis"

    elif not state.is_jd_given:
        return "get_missing_jd"

    elif (state.intent == "" or state.intent is None):
        return "get_missing_intent"