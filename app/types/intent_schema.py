from pydantic import BaseModel, Field

class IntentSchema(BaseModel):
    """
    Schema for capturing user intent and job description details.

    Attributes:
        intent (str): Intent of the user query, either "resume" or "cover_letter".
        is_jd_given (bool): Indicates if a job description is provided.
        job_description (str): The actual job description text (optional).
    """
    intent: str = Field(description="Intent of the user query, i.e. resume or cover_letter")
    is_jd_given: bool = Field(description="Flag to indicate if a job description is provided", default=False)
    job_description: str = Field(description="Job Description", default="")