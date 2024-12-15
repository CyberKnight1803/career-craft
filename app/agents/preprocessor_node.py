from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.prompts.preprocessor_prompt import SYSTEM_PROMPT, PROMPT

from app.types.node_state import NodeState 
from app.types.intent_schema import IntentSchema
from app.config import settings


# Node
class QueryPreprocessorNode:
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
        self.llm = self.llm.with_structured_output(schema=IntentSchema)  

        # Prompt Template 
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", PROMPT)
        ])

    def __call__(self, state: NodeState, config: RunnableConfig) -> Dict[str, Any] | None:

        # Prompt
        prompt = self.prompt_template.invoke({
            "user_query": state.user_query
        })

        print(prompt)

        # Invoke LLM
        output = self.llm.invoke(prompt)

        print(output)

        return {
            "intent": output.intent,
            "is_jd_given": output.is_jd_given,
            "job_description": output.job_description
        }