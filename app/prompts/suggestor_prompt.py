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