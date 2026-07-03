# app/schemas.py

# from pydantic import BaseModel

# class UserCreate(BaseModel):
#     username: str
#     password: str 

# class User(BaseModel):
#     id: int
#     username: str

#     class Config:
#         orm_mode = True

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username: str | None = None

from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: str  # Store MongoDB's ObjectId as a string
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserWithToken(BaseModel):
    user: User
    access_token: str
    token_type: str

    

class Job(BaseModel):
    job_title: str
    company: str
    duration: str
    responsibilities: str

class Project(BaseModel):
    project_title: str
    project_url: str

class Degree(BaseModel):
    degree: Optional[str] = None  # Optional
    institution: Optional[str] = None
    grad_year: Optional[int] = None

class Profile(BaseModel):
    username: Optional[str] = None
    full_name: str
    email_address: str
    phone_number: str
    linkedin_profile_url: Optional[str] = None
    summary: str
    jobs: List[Job]  # List to handle multiple jobs
    projects: List[Project]  # List to handle multiple projects
    degrees: Optional[List[Degree]] = []  # Optional list of degrees
   