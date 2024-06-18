from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, Dict

class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    email: str
    fullname: str
    password: str
    

class Job(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    description: str
    company_name: str
    company_description: str
    company_url: str
    post_url: str
    post_apply: str
    minimum_compensation: float
    maximum_compensation: float
    job_type: str
    role_type: str
    education: str
    original_post: str
    work_location_type: str 
    city: str
    region: str
    country: str 
    published_at: datetime
    updated_at: datetime


def ResponseModel(data: Optional[Dict] = None, message: str = '', status_code: int = 200) -> Dict:
    response = {
        "status_code": status_code,
        "message": message
    }
    if data is not None:
        response["data"] = data
    return response


def ErrorResponseModel(error: str, code: int, message: str) -> Dict:
    return {"error": error, "code": code, "message": message}
