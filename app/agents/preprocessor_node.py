from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

# Importing the custom prompts for query preprocessing
from app.prompts.preprocessor_prompt import SYSTEM_PROMPT, PROMPT

# Importing necessary types for node state and schema
from app.types.node_state import NodeState 
from app.types.intent_schema import IntentSchema
from app.config import settings


# Node for processing user queries
class QueryPreprocessorNode:
    def __init__(
        self,
        model: str = settings.LLM_MODEL,  # Default model from configuration
        temperature: float = settings.TEMPERATURE,  # Temperature for randomness in response
        max_tokens: int = settings.MAX_TOKENS,  # Maximum number of tokens in response
        timeout: float = settings.TIMEOUT  # Timeout for API calls
    ) -> None:
        # Initialize the LLM model with the provided parameters
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout, 
            cache=False  # Disable caching to ensure fresh responses
        )

        # Apply structured output with the specified schema for intent and job description
        self.llm = self.llm.with_structured_output(schema=IntentSchema)

        # Define the prompt template that combines system and human-level prompts
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),  # System-level instructions
            ("human", PROMPT)  # Human-level prompt to guide the query
        ])

    def __call__(self, state: NodeState, config: RunnableConfig) -> Dict[str, Any] | None:
        """
        This method is called when the node is invoked. It processes the user query,
        handles different scenarios for intent and job description, and returns appropriate responses.
        """

        # Case 1: If the intent is provided and job description is not given
        if (state.intent is not None and state.intent != "") and not state.is_jd_given:
            # Generate prompt for LLM based on the last user message
            prompt = self.prompt_template.invoke({
                "user_query": state.messages[-1].content
            })

            # Invoke the LLM with the generated prompt
            output = self.llm.invoke(prompt)
            content = f"Thank you! I will help you craft {state.intent} for the given job description."
            
            # If job description is provided, adjust the response
            if output.is_jd_given:
                content = f"I understand that you want me to help you craft {state.intent}. Can you please provide the job description clearly?" 
            
            # Return response with message, job description, and status of job description
            return {
                "messages": [AIMessage(content=content)],
                "job_description": output.job_description,
                "is_jd_given": output.is_jd_given,
            }

        # Case 2: If intent is not provided and job description is given
        if (state.intent is None or state.intent == "") and state.is_jd_given:
            # Generate prompt for LLM based on the last user message
            prompt = self.prompt_template.invoke({
                "user_query": state.messages[-1].content
            })

            # Invoke the LLM with the generated prompt
            output = self.llm.invoke(prompt)
            content = f"Got it! I will help you craft {output.intent}"
            
            # If no intent is identified, ask for clarification
            if output.intent == "":
                content = "I am sorry, I did not understand that. Can you please provide what do you want me to craft?"

            # Return response with message and detected intent
            return {
                "messages": [AIMessage(content=content)],
                "intent": output.intent,
            }

        # Case 3: Normal flow when intent and job description are both provided or need processing
        prompt = self.prompt_template.invoke({
            "user_query": state.messages[-1].content
        })

        # Invoke LLM to get the output based on the query
        output = self.llm.invoke(prompt)

        print(output)  # Debug print to check the output

        # Determine response content based on the presence of intent and job description
        if (output.intent is not None and output.intent != "") and output.is_jd_given:
            content = f"Got it! I will help you craft {output.intent} for the given job description."
        
        elif (output.intent is not None and output.intent != "") and not output.is_jd_given:
            content = f"I understand that you want me to help you craft {output.intent}. Can you please provide the job description clearly?"
        
        else:
            content = "I am sorry, I did not understand that. Can you please provide what do you want me to craft?"

        # Return the response with message, intent, job description, and status
        return {
            "messages": [AIMessage(content=content)],  # Response message
            "intent": output.intent,  # Identified intent
            "is_jd_given": output.is_jd_given,  # Status if job description is provided
            "job_description": output.job_description  # Job description if available
        }
