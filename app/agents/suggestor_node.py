from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI

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
        self.judge_llm = self.llm.with_structured_output(schema=RatingSchema)
        self.llm = self.llm.with_structured_output(schema=SkillsSchema)

        
        self.exp_prompt_template = ChatPromptTemplate.from_messages([
            ("system", EXP_SYSTEM_PROMPT),
            ("human", EXP_PROMPT)
        ])

        self.proj_prompt_template = ChatPromptTemplate.from_messages([
            ("system", PROJ_SYSTEM_PROMPT),
            ("human", PROJ_PROMPT)
        ])

        self.skills_prompt_template = ChatPromptTemplate.from_messages([
            ("system", SKILLS_SYSTEM_PROMPT),
            ("human", SKILLS_PROMPT)
        ])

    def __call__(self, state: NodeState, config: RunnableConfig) -> Dict[str, Any] | None:
        rated_experiences = []
        for experience in state.user_details["experiences"]:
            prompt = self.exp_prompt_template.invoke({
                "experience": experience,
                "job_description": state.job_description
            })

            output = self.judge_llm.invoke(prompt)
            rated_experiences.append((output.rating, experience))
        
        rated_projects = []
        for project in state.user_details["projects"]:
            prompt = self.proj_prompt_template.invoke({
                "project": project,
                "job_description": state.job_description
            })

            output = self.judge_llm.invoke(prompt)
            rated_projects.append((output.rating, project))
        
        prompt = self.skills_prompt_template.invoke({
            "skills": state.user_details["skills"],
            "job_description": state.job_description
        })

        output = self.llm.invoke(prompt)
        relevant_skills = output.skills

        # Sort and select 
        rated_experiences.sort(reverse=True, key=lambda x: x[0])
        rated_projects.sort(reverse=True, key=lambda x: x[0])

        if (
            (len(rated_experiences) < 2 and len(rated_projects) < 2) or
            (len(rated_experiences) > 2 and len(rated_projects) > 2)
        ):
            state.user_details["experiences"] = [exp for _, exp in rated_experiences[:2]]
            state.user_details["projects"] = [proj for _, proj in rated_projects[:2]]

        elif len(rated_experiences) < 2 and len(rated_projects) >= 2:
            state.user_details["experiences"] = [exp for _, exp in rated_experiences[:2]]

            extra_projects = 2 - len(state.user_details["experiences"])
            state.user_details["projects"] = [proj for _, proj in rated_projects[:2 + extra_projects]]
        
        elif len(rated_experiences) >= 2 and len(rated_projects) < 2:
            state.user_details["projects"] = [proj for _, proj in rated_projects[:2]]

            extra_experiences = 2 - len(state.user_details["projects"])
            state.user_details["experiences"] = [exp for _, exp in rated_experiences[:2 + extra_experiences]]


        state.user_details["skills"] = relevant_skills

        return {
            "user_details": state.user_details
        }
