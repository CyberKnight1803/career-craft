SYSTEM_PROMPT = """
You are an expert at creating highly professional and impactful resume content.
"""

PROMPT = """
Rewrite the experience in the form of concise bullet points with action verbs, relevant keywords, and highlight quantifiable results if possible based on what is relevant and good for the job that is described.

Use the least number of bullet point possible keeping impact in mind. Make sure that there are at max 3 points and that each of them fit in one line.

Experience: 
{experience}
Job Description: 
{job_description}
"""