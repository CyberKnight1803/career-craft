from typing import Dict, Any
import json
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from app.prompts.cl_rephraser_prompt import SYSTEM_PROMPT, PROMPT
from app.types.node_state import NodeState 
from app.config import settings


class CoverLetterRephraserNode:
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
            timeout=timeout, 
            cache=False
        )

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT), 
            ("human", PROMPT)   
        ])



    def __call__(self, state: NodeState, config: RunnableConfig) -> Dict[str, Any] | None:
        prompt = self.prompt_template.invoke({
            "position": state.job_description.position,
            "organization": state.job_description.organization,
            "job_responsibilities": state.job_description.responsibilities, 
            "job_skills": state.job_description.skills,
            "user_skills": state.user_details["skills"], 
            "user_experiences": json.dumps(state.user_details["experiences"], indent=2), 
            "user_education": json.dumps(state.user_details["education"], indent=2),
            "user_projects": json.dumps(state.user_details["projects"], indent=2), 
            "user_details": json.dumps(state.user_details, indent=2),
            "date": datetime.now().strftime("%b %d, %Y")
        })

        output = self.llm.invoke(prompt)

        return {
            "messages": [AIMessage(content="Crafted your cover letter!")],
            "cover_letter": output.content
        }