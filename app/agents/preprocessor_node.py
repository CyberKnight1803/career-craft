from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage
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

        if (state.intent is not None and state.intent != "") and not state.is_jd_given:
            prompt = self.prompt_template.invoke({
                "user_query": state.messages[-1].content
            })

            # Invoke LLM
            output = self.llm.invoke(prompt)
            content = f"Thank you! I will help you craft {state.intent} for the given job description."
            if output.is_jd_given:
                content = f"I understand that you want me to help you craft {state.intent}. Can you please provide the job description clearly?" 
            
            return {
                "messages": [AIMessage(content=content)],
                "job_description": output.job_description,
                "is_jd_given": output.is_jd_given,
            }
    
        if (state.intent is None or state.intent == "") and state.is_jd_given:
            prompt = self.prompt_template.invoke({
                "user_query": state.messages[-1].content
            })

            # Invoke LLM
            output = self.llm.invoke(prompt)
            content = f"Got it! I will help you craft {output.intent}"
            if output.intent == "":
                content = "I am sorry, I did not understand that. Can you please provide what do you want me to craft?"

            return {
                "messages": [AIMessage(content=content)],
                "intent": output.intent,
            } 


        # Normal

        prompt = self.prompt_template.invoke({
            "user_query": state.messages[-1].content
        })

        # Invoke LLM
        output = self.llm.invoke(prompt)

        print(output)

        if (output.intent is not None and output.intent != "") and output.is_jd_given:
            content = f"Got it! I will help you craft {output.intent} for the given job description."
        
        elif (output.intent is not None and output.intent != "") and not output.is_jd_given:
            content = f"I understand that you want me to help you craft {output.intent}. Can you please provide the job description clearly?"
        
        else:
            content = "I am sorry, I did not understand that. Can you please provide what do you want me to craft?"

        return {
            "messages": [AIMessage(content=content)],
            "intent": output.intent,
            "is_jd_given": output.is_jd_given,
            "job_description": output.job_description
        }