from typing import List, TypedDict, Optional
from pydantic import BaseModel, Field

class PersonalDetails(TypedDict): 
    name: str 
    email: str 
    phone: str 
    location: str 
    linkedin: str 
    github: str

class Education(TypedDict):
    grad_date: str 
    institution: str
    degree: str 
    gpa: str 
    courses: List[str] 
    summary: Optional[str]

class Experience(TypedDict):
    start_date: str
    end_date: str 
    organization: str
    location: str
    position: str
    description: List[str] 
    skills: Optional[List[str]]

class Project(TypedDict):
    start_date: str
    end_date: str 
    name: str
    description: List[str]
    skills: Optional[List[str]]
    github_link: Optional[str]
    resume_link: Optional[str]

class Skills(TypedDict):
    languages: List[str]
    frameworks: List[str]
    tools: List[str] 

class Certificate(TypedDict): 
    name: str 
    link: str

class UserDetails(BaseModel):
    personal_details: PersonalDetails = Field(description="Personal Details", default=None)
    education: List[Education] = Field(description="Education Details", default=[])
    experience: List[Experience] = Field(description="Experience Details", default=[])
    projects: List[Project] = Field(description="Project Details", default=[])
    skills: Skills = Field(description="Skills", default=None)
    certificates: Optional[List[Certificate]] = Field(description="Certifications", default=[])
