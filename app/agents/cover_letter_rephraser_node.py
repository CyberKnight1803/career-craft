from typing import Dict, Any
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.types.node_state import NodeState 
from app.config import settings


class CoverLetterRephraserNode:
    def __init__(self):
        pass 

    def __call__(self, state: NodeState, config: RunnableConfig) -> Dict[str, Any] | None:
        return None
