from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.types import interrupt
from langchain_openai import ChatOpenAI

# Importing custom prompts and types
from app.prompts.jda_prompt import SYSTEM_PROMPT, PROMPT
from app.types.jd_schema import JDSchema
from app.types.node_state import NodeState
from app.config import settings


class JDANode:
    def __init__(
        self,
        model: str = settings.LLM_MODEL,  # Default model set from config settings
        temperature: float = settings.TEMPERATURE,  # Temperature for randomness in response
        max_tokens: int = settings.MAX_TOKENS,  # Maximum number of tokens for the response
        timeout: float = settings.TIMEOUT  # Timeout setting for the API call
    ) -> None:
        # Initialize the LLM with the provided settings
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout
        )

        # Apply structured output configuration to the LLM with a defined schema (JDSchema)
        self.llm = self.llm.with_structured_output(schema=JDSchema)

        # Define the prompt template with system and human prompt components
        self.prompt_template = ChatPromptTemplate([
            ("system", SYSTEM_PROMPT),  # System-level instructions for the model
            ("human", PROMPT)  # The prompt text for the human input (job description)
        ]) 

    def __call__(self, state: NodeState, config: RunnableConfig) -> Dict[str, Any] | None:
        """
        This method is called when the node is invoked in the flow. It takes the current state
        and configuration as inputs, processes the job description, and generates a structured
        job description response.
        """
        
        # Create the prompt by inserting the job description from the state into the template
        prompt = self.prompt_template.invoke({
            "job_description": state.job_description  # Use the job description from the node state
        })

        # Use the LLM to generate the structured job description response based on the prompt
        structured_jd = self.llm.invoke(prompt)
        
        # Return the result with a flag indicating that a job description was processed
        return {
            "is_jd_given": True,  # Indicate that the job description was provided
            "job_description": structured_jd  # Return the structured job description
        }
