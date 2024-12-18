from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI

# Import custom prompts and types for experience, project, and skills evaluation
from app.prompts.suggestor_prompt import (
    EXP_SYSTEM_PROMPT, EXP_PROMPT,
    PROJ_SYSTEM_PROMPT, PROJ_PROMPT,
    SKILLS_SYSTEM_PROMPT, SKILLS_PROMPT
)
from app.types.suggestor_schema import RatingSchema, SkillsSchema
from app.types.node_state import NodeState 
from app.config import settings

class SuggestorNode:
    def __init__(
        self,
        model: str = settings.LLM_MODEL,  # LLM model from settings
        temperature: float = settings.TEMPERATURE,  # Temperature for randomness in output
        max_tokens: int = settings.MAX_TOKENS,  # Max number of tokens for the output
        timeout: float = settings.TIMEOUT  # Timeout for the API call
    ) -> None:
        # Initialize the LLM with the provided settings
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout, 
            cache=False  # Disable cache for fresh responses
        ) 

        # Structured Output for judging experiences and skills using defined schemas
        self.judge_llm = self.llm.with_structured_output(schema=RatingSchema)  # Ratings for experiences and projects
        self.llm = self.llm.with_structured_output(schema=SkillsSchema)  # Skills output

        # Define prompt templates for different categories: experiences, projects, and skills
        self.exp_prompt_template = ChatPromptTemplate.from_messages([
            ("system", EXP_SYSTEM_PROMPT),  # System-level instructions for experience evaluation
            ("human", EXP_PROMPT)  # Human-level prompt for experience evaluation
        ])

        self.proj_prompt_template = ChatPromptTemplate.from_messages([
            ("system", PROJ_SYSTEM_PROMPT),  # System-level instructions for project evaluation
            ("human", PROJ_PROMPT)  # Human-level prompt for project evaluation
        ])

        self.skills_prompt_template = ChatPromptTemplate.from_messages([
            ("system", SKILLS_SYSTEM_PROMPT),  # System-level instructions for skill evaluation
            ("human", SKILLS_PROMPT)  # Human-level prompt for skill evaluation
        ])

    def __call__(self, state: NodeState, config: RunnableConfig) -> Dict[str, Any] | None:
        """
        This method processes the user’s experiences, projects, and skills to determine the most relevant details
        for a specific job description. It evaluates the experiences and projects, rates them, and filters the 
        most relevant skills to return an updated version of the user's details.
        """
        
        rated_experiences = []  # List to store rated experiences
        # Evaluate and rate each experience based on the job description
        for experience in state.user_details["experiences"]:
            prompt = self.exp_prompt_template.invoke({
                "experience": experience,  # The user’s experience to be evaluated
                "job_description": state.job_description  # The job description for context
            })

            # Get the rating and append the experience with its rating
            output = self.judge_llm.invoke(prompt)
            rated_experiences.append((output.rating, experience))
        
        rated_projects = []  # List to store rated projects
        # Evaluate and rate each project based on the job description
        for project in state.user_details["projects"]:
            prompt = self.proj_prompt_template.invoke({
                "project": project,  # The user’s project to be evaluated
                "job_description": state.job_description  # The job description for context
            })

            # Get the rating and append the project with its rating
            output = self.judge_llm.invoke(prompt)
            rated_projects.append((output.rating, project))
        
        # Evaluate the relevance of skills to the job description
        prompt = self.skills_prompt_template.invoke({
            "skills": state.user_details["skills"],  # The user’s skills to be evaluated
            "job_description": state.job_description  # The job description for context
        })

        output = self.llm.invoke(prompt)
        relevant_skills = output.skills  # Extract relevant skills for the job description

        # Sort experiences and projects by rating in descending order
        rated_experiences.sort(reverse=True, key=lambda x: x[0])
        rated_projects.sort(reverse=True, key=lambda x: x[0])

        # Logic to update the user's experiences and projects based on the ratings
        if (
            (len(rated_experiences) < 2 and len(rated_projects) < 2) or  # Less than 2 experiences and projects
            (len(rated_experiences) > 2 and len(rated_projects) > 2)  # More than 2 experiences and projects
        ):
            # Select top 2 rated experiences and projects
            state.user_details["experiences"] = [exp for _, exp in rated_experiences[:2]]
            state.user_details["projects"] = [proj for _, proj in rated_projects[:2]]

        elif len(rated_experiences) < 2 and len(rated_projects) >= 2:
            # Select 2 experiences, and the remaining required number of projects
            state.user_details["experiences"] = [exp for _, exp in rated_experiences[:2]]
            extra_projects = 2 - len(state.user_details["experiences"])
            state.user_details["projects"] = [proj for _, proj in rated_projects[:2 + extra_projects]]
        
        elif len(rated_experiences) >= 2 and len(rated_projects) < 2:
            # Select 2 projects, and the remaining required number of experiences
            state.user_details["projects"] = [proj for _, proj in rated_projects[:2]]
            extra_experiences = 2 - len(state.user_details["projects"])
            state.user_details["experiences"] = [exp for _, exp in rated_experiences[:2 + extra_experiences]]

        # Update skills with the most relevant skills for the job description
        state.user_details["skills"] = relevant_skills

        # Return the updated user details with the most relevant experiences, projects, and skills
        return {
            "user_details": state.user_details
        }
