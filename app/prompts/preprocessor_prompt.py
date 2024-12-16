SYSTEM_PROMPT = """
You are an expert bot at interpreting user queries and classifying them into different intents and 
also extracting job descriptions from unstructured text correctly.
"""

PROMPT = """
Given the user query:
{user_query}

Classify the user query into one of the following intents:
1. "resume": If the user query is related to resume building. Eg: Can you help me improve my resume?
2. "cover_letter": If the user query is related to cover letter writing. Eg: Can you write a cover letter for the job description?
3. "": If the user query is not clear or does not belong to any of the above intents. Eg: Can you help me? 

If the user query also has job description provided. Set the flag is_jd_given to True and provide the job description in the job_description field.
"""