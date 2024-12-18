from typing import Literal
from langchain_core.runnables import RunnableConfig
from langgraph.types import interrupt, Command

from app.types.node_state import NodeState

# Function to handle document type decision
def handle_doc_type(state: NodeState, config: RunnableConfig) -> Literal["resume_rephraser", "cover_letter_rephraser"]:
    """
    Determines the next step based on the user's intent.
    
    Args:
        state (NodeState): The current state object containing user input and inferred data.
        config (RunnableConfig): Configuration object for the runnable node.

    Returns:
        Literal["resume_rephraser", "cover_letter_rephraser"]: The next node to process the request.
    """
    if state.intent == "resume": 
        return "resume_rephraser"  # Route to the resume rephraser node.

    elif state.intent == "cover_letter":
        return "cover_letter_rephraser"  # Route to the cover letter rephraser node.

# Function to handle missing information
def handle_missing_info(state: NodeState, config: RunnableConfig) -> Literal["get_missing_jd", "get_missing_intent", "jd_analysis"]:
    """
    Handles scenarios where certain inputs (job description or intent) are missing and determines the next step.
    
    Args:
        state (NodeState): The current state object containing user input and inferred data.
        config (RunnableConfig): Configuration object for the runnable node.

    Returns:
        Literal["get_missing_jd", "get_missing_intent", "jd_analysis"]: The next node to handle the missing information or proceed with analysis.
    """
    if state.is_jd_given and (state.intent != "" and state.intent is not None):
        return "jd_analysis"  # Proceed to job description analysis.

    elif not state.is_jd_given:
        return "get_missing_jd"  # Route to the node for obtaining missing job description.

    elif (state.intent == "" or state.intent is None):
        return "get_missing_intent"  # Route to the node for obtaining missing intent.
