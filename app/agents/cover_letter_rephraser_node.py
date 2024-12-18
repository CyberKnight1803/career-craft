# Importing necessary libraries
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
    """
    A node responsible for rephrasing a cover letter based on the provided job description 
    and user's skills, experience, education, and projects. Uses a language model (LLM) to 
    generate a refined cover letter tailored to the job position and organization.

    Attributes:
        model (str): The name of the language model to be used.
        temperature (float): The temperature setting for the LLM to control randomness.
        max_tokens (int): Maximum number of tokens to be generated in the output.
        timeout (float): Timeout value for the LLM request.
        llm (ChatOpenAI): Instance of the LLM for generating the output.
        prompt_template (ChatPromptTemplate): Template for structuring the input prompt.
    """

    def __init__(
        self, 
        model: str = settings.LLM_MODEL,
        temperature: float = settings.TEMPERATURE,
        max_tokens: int = settings.MAX_TOKENS,
        timeout: float = settings.TIMEOUT
    ) -> None:
        """
        Initializes the CoverLetterRephraserNode with the specified settings.

        Args:
            model (str): The LLM model to use (default from settings).
            temperature (float): The temperature for the LLM (default from settings).
            max_tokens (int): The maximum number of tokens for the LLM response.
            timeout (float): Timeout value for the LLM response.
        """
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout, 
            cache=False  # Ensures fresh responses without caching
        )

        # Define the prompt template with system and human messages.
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),  # Instructions for the LLM.
            ("human", PROMPT)  # Input from the user to guide the response.
        ])

    def __call__(self, state: NodeState, config: RunnableConfig) -> Dict[str, Any] | None:
        """
        Generates a rephrased cover letter using the LLM.

        Args:
            state (NodeState): The current state containing job description, user details, etc.
            config (RunnableConfig): Additional runtime configurations.

        Returns:
            Dict[str, Any] | None: A dictionary containing the generated cover letter and 
            a message for the user, or None if generation fails.
        """
        # Prepare the input prompt for the LLM using state data.
        prompt = self.prompt_template.invoke({
            "position": state.job_description.position,  # Job title.
            "organization": state.job_description.organization,  # Organization name.
            "job_responsibilities": state.job_description.responsibilities,  # Job responsibilities.
            "job_skills": state.job_description.skills,  # Required skills from the job description.
            "user_skills": state.user_details["skills"],  # User's skills.
            "user_experiences": json.dumps(state.user_details["experiences"], indent=2),  # User's experiences.
            "user_education": json.dumps(state.user_details["education"], indent=2),  # User's education details.
            "user_projects": json.dumps(state.user_details["projects"], indent=2),  # User's projects.
            "user_details": json.dumps(state.user_details, indent=2),  # Full user details in JSON format.
            "date": datetime.now().strftime("%b %d, %Y")  # Current date for use in the cover letter.
        })

        # Invoke the LLM with the prepared prompt and capture the output.
        output = self.llm.invoke(prompt)

        # Return the generated cover letter and an acknowledgment message.
        return {
            "messages": [AIMessage(content="Crafted your cover letter!")],  # Message to indicate success.
            "cover_letter": output.content  # Generated cover letter content.
        }
