import pandas as pd
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from deepeval import assert_test
from deepeval.test_case import LLMTestCaseParams, LLMTestCase
from deepeval.metrics import GEval
from typing import Dict, List

# Load Dataset
DATASET_CSV = "job_description_testcases.csv"

SYSTEM_PROMPT = """
You're an expert bot who can extract the unstructured job description 
provided by the user into a structured format. 
"""

PROMPT = """
Extract the job description as per the following structure: 
Rules: 
1. Set position as the job title extracted from the job description.
2. Set organization as the company name extracted from the job description.
4. Set responsibilities as a list of summarized responsibilities extracted from the job description.
5. Set skills as a list of skills extracted from the job description. Skills are languages or frameworks or tools used. Eg: (python, java, github, pytorch, docker, etc)

Extract the job description in structured format from the unstructured description provided below: 
{job_description}
"""

class JDSchema(BaseModel):
    position: str = Field(description="Job Title")
    organization: str = Field(description="Organization")
    responsibilities: List[str] = Field(description="Summarized Responsibilities")
    skills: List[str]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.0, 
    max_tokens=4096,
    timeout=300
)

llm = llm.with_structured_output(schema=JDSchema)
prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", PROMPT)
])

def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def mock_llm_call(job_description: str) -> Dict[str, str]:
    """
    Mock function for LLM API calls.
    """
    
    prompt = prompt_template.invoke({
        "job_description": job_description
    })

    structured_jd = llm.invoke(prompt)

    return {
        "position": structured_jd.position,
        "organization": structured_jd.organization,
        "summarized_responsibilities": structured_jd.responsibilities,
        "skills": structured_jd.skills
    }

def evaluate_extraction_accuracy():
    # Load test data
    df = load_data(DATASET_CSV)
    
    # Define LLMJudgeMetric
    llm_judge_metric = GEval(
        name="Extraction Accuracy",  
        criteria="Determine if extracted job description fields are accurate based on the given job description",
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT]
    )

    for idx, row in df.iterrows():
        job_description = row['job_description']
        expected = {
            "position": row['expected_position'],
            "organization": row['expected_organization'],
            "summarized_responsibilities": row['expected_summarized_responsibilities'],
            "skills": row['expected_skills']
        }

        # Actual Extraction (using LLM call)
        actual = mock_llm_call(job_description)
        
        # Evaluate with LLMJudgeMetric
        for key in expected:
            test = LLMTestCase(
                name=f"{key}_extraction_test_case_{idx}",
                input=job_description,
                actual_output=actual[key],
                expected_output=expected[key],
                metrics=[llm_judge_metric]
            )
            
            # Run and Assert Test
            assert_test(test)
            print(f"{key.capitalize()} Test {idx}: Passed")

if __name__ == "__main__":
    evaluate_extraction_accuracy()
