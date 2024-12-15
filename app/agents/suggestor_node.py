from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.prompts.suggestor_prompt import SYSTEM_PROMPT, PROMPT
from app.types.suggestor_schema import SuggestorSchema
from app.types.node_state import NodeState 
from app.config import settings

class SuggestorNode:
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

        # Structured Output
        self.llm = self.llm.with_structured_output(schema=SuggestorSchema)

        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT), 
            ("human", PROMPT)
        ])


    def __call__(self, state: NodeState, config: RunnableConfig) -> Dict[str, Any] | None:
        
        prompt = self.prompt_template.invoke({
            "job_description": state.job_description,
            "experiences": state.user_details["experiences"],
            "projects": state.user_details["projects"],
            "skills": state.user_details["skills"]
        })

        print("SUGGESTOR PROMPT")
        print(prompt)
        print("\n\n\n\n")

        output = self.llm.invoke(prompt)

        print("LLM RESPONSE")
        print(output)

        state.user_details["experiences"] = output.experiences
        state.user_details["projects"] = output.projects
        state.user_details["skills"] = output.skills


        return {
            "user_details": state.user_details
        } 
