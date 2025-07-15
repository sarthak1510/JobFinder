from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

class JobModel(BaseModel):
    title: str
    company: Optional[str]
    location: Optional[str]
    description: str
    redirect_url: HttpUrl = Field(..., alias="url")
