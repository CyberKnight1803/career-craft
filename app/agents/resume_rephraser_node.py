from typing import Dict, Any
from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.prompts.resume_rephraser_prompt import (
    SYSTEM_PROMPT, PROMPT
)

from app.types.node_state import NodeState 
from app.types.enhancer_schema import EnhancerSchema
from app.config import settings


class ResumeRephraserNode:
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

        self.llm = self.llm.with_structured_output(schema=EnhancerSchema)

         # Prompt Template
        self.enhanced_bullet_points_prompt_template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", PROMPT)
        ])

    def rephrase_description(self, description_points: list[str], job_description: str) -> list[str]:
        """
        Rephrases a list of description points to make them concise, impactful, and relevant to the job.
        """
        original_description = ""
        for point in description_points:
            original_description += point

        prompt = self.enhanced_bullet_points_prompt_template.invoke({
            "experience": original_description,
            "job_description": job_description
        })

        output = self.llm.invoke(prompt)

        return output.enhanced_points

    def process_experiences(self, experiences: list[Dict[str, Any]], job_description: str) -> list[Dict[str, Any]]:
        """
        Processes and enhances the descriptions in the experiences.
        """
        for experience in experiences:
            if "description" in experience and isinstance(experience["description"], list):
                experience["description"] = self.rephrase_description(
                    experience["description"], job_description
                )
        return experiences

    def process_projects(self, projects: list[Dict[str, Any]], job_description: str) -> list[Dict[str, Any]]:
        """
        Processes and enhances the descriptions in the projects.
        """
        for project in projects:
            if "description" in project and isinstance(project["description"], list):
                project["description"] = self.rephrase_description(
                    project["description"], job_description
                )
        return projects

    def __call__(self, state: NodeState, config: RunnableConfig) -> Dict[str, Any] | None:

        user_details = state.user_details
        job_description = state.job_description

        if not user_details or not job_description:
            return None

        # Process experiences
        if "experience" in user_details:
            user_details["experience"] = self.process_experiences(
                user_details["experience"], job_description
            )

        # Process projects
        if "projects" in user_details:
            user_details["projects"] = self.process_projects(
                user_details["projects"], job_description
            )

        return {
            "user_details": user_details
        }

