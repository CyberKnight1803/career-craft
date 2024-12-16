from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.types import interrupt
from langchain_openai import ChatOpenAI

from app.prompts.jda_prompt import SYSTEM_PROMPT, PROMPT
from app.types.jd_schema import JDSchema
from app.types.node_state import NodeState
from app.config import settings


class JDANode:
    def __init__(
        self,
        model: str = settings.LLM_MODEL,
        temperature: float = settings.TEMPERATURE,
        max_tokens: int = settings.MAX_TOKENS,
        timeout: float = settings.TIMEOUT
    ) -> None:

        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout
        )

        self.llm = self.llm.with_structured_output(schema=JDSchema)

        # Prompt Template
        self.prompt_template = ChatPromptTemplate([
            ("system", SYSTEM_PROMPT),
            ("human", PROMPT)
        ]) 

    def __call__(self, state: NodeState, config: RunnableConfig) -> Dict[str, Any] | None:
        
        prompt = self.prompt_template.invoke({
            "job_description": state.job_description
        })

        structured_jd = self.llm.invoke(prompt)
        
        return {
            "is_jd_given": True,
            "job_description": structured_jd
        }
