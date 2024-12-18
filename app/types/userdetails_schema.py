from typing import List, TypedDict, Optional
from pydantic import BaseModel, Field

class PersonalDetails(TypedDict): 
    """
    Schema for storing personal details of the user.
    """
    name: str 
    email: str 
    phone: str 
    location: str 
    linkedin: str 
    github: str

class Education(TypedDict):
    """
    Schema for storing education details.
    """
    grad_date: str 
    institution: str
    degree: str 
    gpa: str 
    courses: List[str] 
    summary: Optional[str]

class Experience(TypedDict):
    """
    Schema for storing professional experience details.
    """
    start_date: str
    end_date: str 
    organization: str
    location: str
    position: str
    description: List[str] 
    skills: Optional[List[str]]

class Project(TypedDict):
    """
    Schema for storing project details.
    """
    start_date: str
    end_date: str 
    name: str
    description: List[str]
    skills: Optional[List[str]]
    github_link: Optional[str]
    resume_link: Optional[str]

class Skills(TypedDict):
    """
    Schema for storing skill categories.
    """
    languages: List[str]
    frameworks: List[str]
    tools: List[str] 

class Certificate(TypedDict): 
    """
    Schema for storing certification details.
    """
    name: str 
    link: str

class UserDetails(BaseModel):
    """
    Schema for storing complete user details.
    """
    personal_details: PersonalDetails = Field(description="Personal Details", default=None)
    education: List[Education] = Field(description="Education Details", default=[])
    experience: List[Experience] = Field(description="Experience Details", default=[])
    projects: List[Project] = Field(description="Project Details", default=[])
    skills: Skills = Field(description="Skills", default=None)
    certificates: Optional[List[Certificate]] = Field(description="Certifications", default=[])
