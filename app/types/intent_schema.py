from pydantic import BaseModel, Field

class IntentSchema(BaseModel):
    intent: str = Field(description="Intent of the user query, i.e. resume or cover_letter")
    is_jd_given: bool = Field(description="Flag to indicate if a job description is provided", default=False)
    job_description: str = Field(description="Job Description", default="")