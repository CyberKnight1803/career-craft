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