from typing import Dict, Any
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Importing custom prompts for resume rephrasing
from app.prompts.resume_rephraser_prompt import (
    SYSTEM_PROMPT, PROMPT
)

# Importing necessary types for node state and schema
from app.types.node_state import NodeState 
from app.types.enhancer_schema import EnhancerSchema
from app.config import settings


class ResumeRephraserNode:
    def __init__(
        self,
        model: str = settings.LLM_MODEL,  # Default model from config
        temperature: float = settings.TEMPERATURE,  # Temperature for output randomness
        max_tokens: int = settings.MAX_TOKENS,  # Max tokens for LLM output
        timeout: float = settings.TIMEOUT  # Timeout for the API request
    ) -> None:
        
        # Initialize the LLM model with the provided settings
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout, 
            cache=False  # Disable cache to ensure fresh results
        )

        # Apply structured output with the specified schema for enhanced points
        self.llm = self.llm.with_structured_output(schema=EnhancerSchema)

        # Define the prompt template for enhancing bullet points in resume descriptions
        self.enhanced_bullet_points_prompt_template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),  # System-level instructions for the rephrasing task
            ("human", PROMPT)  # Human-level prompt for input description
        ])

    def rephrase_description(self, description_points: list[str], job_description: str) -> list[str]:
        """
        Rephrases a list of description points to make them concise, impactful, and relevant to the job.
        Takes in a list of description points and a job description to tailor the content.
        """
        original_description = ""  # Initialize an empty string to concatenate the points
        for point in description_points:
            original_description += point  # Concatenate all points into a single string

        # Create the prompt by combining the experience description and job description
        prompt = self.enhanced_bullet_points_prompt_template.invoke({
            "experience": original_description,  # User's experience points
            "job_description": job_description  # Job description for context
        })

        # Invoke the LLM to get the enhanced description points
        output = self.llm.invoke(prompt)

        # Return the enhanced and rephrased points
        return output.enhanced_points

    def process_experiences(self, experiences: list[Dict[str, Any]], job_description: str) -> list[Dict[str, Any]]:
        """
        Processes and enhances the descriptions in the experiences.
        Iterates over the list of experiences and applies the rephrasing function.
        """
        for experience in experiences:
            # If experience has a description and it's a list of points, rephrase it
            if "description" in experience and isinstance(experience["description"], list):
                experience["description"] = self.rephrase_description(
                    experience["description"], job_description  # Rephrase using job description
                )
        return experiences

    def process_projects(self, projects: list[Dict[str, Any]], job_description: str) -> list[Dict[str, Any]]:
        """
        Processes and enhances the descriptions in the projects.
        Similar to experiences, applies the rephrasing function to project descriptions.
        """
        for project in projects:
            # If project has a description and it's a list of points, rephrase it
            if "description" in project and isinstance(project["description"], list):
                project["description"] = self.rephrase_description(
                    project["description"], job_description  # Rephrase using job description
                )
        return projects

    def __call__(self, state: NodeState, config: RunnableConfig) -> Dict[str, Any] | None:
        """
        This method is called when the node is invoked. It processes user details (experiences and projects),
        rephrasing them based on the job description and returning the updated user details.
        """
        user_details = state.user_details  # Extract user details from the state
        job_description = state.job_description  # Extract job description from the state

        # If either user details or job description is missing, return None
        if not user_details or not job_description:
            return None

        # Process experiences if available
        if "experience" in user_details:
            user_details["experience"] = self.process_experiences(
                user_details["experience"], job_description  # Rephrase experiences
            )

        # Process projects if available
        if "projects" in user_details:
            user_details["projects"] = self.process_projects(
                user_details["projects"], job_description  # Rephrase projects
            )

        # Return the updated user details
        return {
            "user_details": user_details  # Return the enhanced user details
        }