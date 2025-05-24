from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PromptCreate(BaseModel):
    input_text: str

class PromptResponse(PromptCreate):
    id: int
    user_id: int
    blog_output: str
    created_at: datetime

    class Config:
        from_attributes = True

class SocialPostPreview(BaseModel):
    facebook: str
    linkedin: str

class PostLogCreate(BaseModel):
    prompt_id: int
    platform: str
    content: str

class PostLogResponse(PostLogCreate):
    id: int
    user_id: int
    status: str
    error: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True 