from typing import Dict, Any
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.types.node_state import NodeState 
from app.config import settings


def get_missing_jd(state: NodeState, config: RunnableConfig) -> Dict[str, Any] | None:
    pass 

def get_missing_intent(state: NodeState, config: RunnableConfig) -> Dict[str, Any] | None:
    pass 