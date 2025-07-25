"""
schemas.py
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class InteractionCreate(BaseModel):
    message: str
    response: str

class InteractionOut(BaseModel):
    id: int
    message: str
    response: str
    timestamp: datetime
    class Config:
        orm_mode = True

class CycleCreate(BaseModel):
    start_date: datetime
    symptoms: Optional[str] = None
    moods: Optional[str] = None

class CycleOut(BaseModel):
    id: int
    start_date: datetime
    symptoms: Optional[str]
    moods: Optional[str]
    class Config:
        orm_mode = True

class ReminderCreate(BaseModel):
    type: str
    time: str
    method: str

class ReminderOut(BaseModel):
    id: int
    type: str
    time: str
    method: str
    active: bool
    class Config:
        orm_mode = True

class PartnerInvite(BaseModel):
    partner_email: EmailStr
    consent_type: str

class PartnerOut(BaseModel):
    id: int
    partner_user_id: int
    consent_type: str
    status: str
    class Config:
        orm_mode = True 