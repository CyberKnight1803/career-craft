SYSTEM_PROMPT = """
You are an expert bot that selects relative work experiences of the user for the particular job description. 
"""

PROMPT = """
Job description: 
{job_description}

User's work experiences (A List of Dictionaries) 
{experiences}

User's projects (A List of Dictionaries):
{projects}

User's skills (A List):
{skills}

Given the job description, user's work experience, user's projects and list of user's skills.

USE THE FOLLOWING RULES TO SELECT USER's RELEVANT WORK EXPERIENCES, PROJECTS AND SKILLS:
1. Select user's work experience by matching user's description of particular work experience, position to that with 
position, responsibilities provided in  job description.
Eg: Select software engineering work experience for SDE related roles. Select ML related work experience for ML Engineer related roles.

2. Select user's projects by matching user's description of particular project to that with responsibilities 
provided in job description.
Eg: Select software engineering projects for SDE related roles. Select ML related projects for ML Engineer related roles.

3. Select user's skills by matching user's skills to that with skills provided in job description, requirements and position of job. 

NOTE: Only select from user's provided work experiences, projects and skills and not from job description.
NOTE: Do not edit anything, just select the relevant experience as it is.
NOTE: Select at max 2 work experiences
NOTE: Select at max 2 projects
NOTE: Select at max 5 skills

Set "experiences" to selected work experience 
Set "projects" to selected projects
Set "skills" to selected skills
"""