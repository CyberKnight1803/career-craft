import pandas as pd
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from deepeval import assert_test
from deepeval.test_case import LLMTestCaseParams, LLMTestCase
from deepeval.metrics import GEval
from typing import Dict, List

EXP_SYSTEM_PROMPT = """
You're an expert judge who can give high quality rating for user's work experience to the given job description. 
A high score indicates that the user's work experience is highly relevant to the job description and vice-versa.
"""

EXP_PROMPT = """
Rate out of 10 for the given user's work experience to the job description provided below:

User's Work Experience:
{experience}

Job Description:
{job_description}

Analyze and give a score out of 0-10. 
"""

PROJ_SYSTEM_PROMPT = """
You're an expert judge who can give high quality rating for user's project to the given job description.
A high score indicates that the user's project is highly relevant to the job description and vice-versa.
"""

PROJ_PROMPT = """
Rate out of 10 for the given user's project to the job description provided below:

User's Project:
{project}

Job Description:
{job_description}

Analyze and give a score out of 0-10. 
"""

SKILLS_SYSTEM_PROMPT = """
You're an expert judge who can select the relevant skills for the given job description.
"""

SKILLS_PROMPT = """
Select all the top 10 relevant user's skills for the job description provided below:

User's skills: 
{skills}

Job Description:
{job_description}

NOTE: Select top 10 skills only.
"""

DATASET_CSV = "job_description_testcases.csv"

class ResumeTestCase(BaseModel):
    job_description: str = Field(..., description="The job description")
    experiences: List[str] = Field(..., description="List of user's work experiences")
    projects: List[str] = Field(..., description="List of user's projects")
    selected_experiences: List[str] = Field(..., description="Top 2 suggested experiences")
    selected_projects: List[str] = Field(..., description="Top 2 suggested projects")
    skills: List[str] = Field(..., description="List of user's skills")

# Initialize LangChain ChatOpenAI
llm = ChatOpenAI(model="gpt-4", temperature=0)

def run_prompt(prompt_template: str, system_message: str, **kwargs) -> str:
    """
    Run a ChatOpenAI prompt using LangChain templates.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", prompt_template)
    ])
    formatted_prompt = prompt.format(**kwargs)
    return llm.predict(formatted_prompt)

def evaluate_experiences(job_description: str, experiences: List[str], selected_experiences: List[str]) -> float:
    """
    Evaluate selected experiences for alignment with the job description.
    """
    total_score = 0
    for exp in selected_experiences:
        score = run_prompt(EXP_PROMPT, EXP_SYSTEM_PROMPT, experience=exp, job_description=job_description)
        total_score += float(score)
    return total_score / len(selected_experiences)

def evaluate_projects(job_description: str, projects: List[str], selected_projects: List[str]) -> float:
    """
    Evaluate selected projects for alignment with the job description.
    """
    total_score = 0
    for proj in selected_projects:
        score = run_prompt(PROJ_PROMPT, PROJ_SYSTEM_PROMPT, project=proj, job_description=job_description)
        total_score += float(score)
    return total_score / len(selected_projects)

def evaluate_resume_alignment(test_case: ResumeTestCase):
    """
    Evaluate alignment of experiences and projects with job description.
    """
    exp_score = evaluate_experiences(test_case.job_description, test_case.experiences, test_case.selected_experiences)
    proj_score = evaluate_projects(test_case.job_description, test_case.projects, test_case.selected_projects)

    print(f"Experience Alignment Score: {exp_score:.2f}/10")
    print(f"Project Alignment Score: {proj_score:.2f}/10")
    return (exp_score, proj_score)

def evaluate_dataset():
    df = pd.read_csv(DATASET_CSV)
    for idx, row in df.iterrows():
        test_case = ResumeTestCase(
            job_description=row['job_description'],
            experiences=eval(row['experiences']),
            projects=eval(row['projects']),
            selected_experiences=eval(row['selected_experiences']),
            selected_projects=eval(row['selected_projects']),
            skills=eval(row['skills'])
        )
        
        exp_score, proj_score = evaluate_resume_alignment(test_case)
        
        # Create and assert test case for evaluation
        llm_test_case = LLMTestCase(
            params=LLMTestCaseParams(
                input=test_case.job_description,
                actual_output=f"Experience Score: {exp_score:.2f}, Project Score: {proj_score:.2f}",
                expected_output="High relevance scores for selected experiences and projects",
            ),
            metrics=[GEval(criteria="accuracy")]
        )
        assert_test(llm_test_case)
        print(f"Test Case {idx + 1}: Passed\n")

if __name__ == "__main__":
    evaluate_dataset()