"""
models.py
SQLAlchemy models for CycleWise backend.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    interactions = relationship("Interaction", back_populates="user")
    cycles = relationship("Cycle", back_populates="user")
    reminders = relationship("Reminder", back_populates="user")
    partners = relationship("Partner", back_populates="user", foreign_keys='Partner.user_id')
    partner_of = relationship("Partner", back_populates="partner", foreign_keys='Partner.partner_user_id')

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="interactions")

class Cycle(Base):
    __tablename__ = "cycles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(DateTime, nullable=False)
    symptoms = Column(Text)
    moods = Column(Text)
    
    user = relationship("User", back_populates="cycles")

class Reminder(Base):
    __tablename__ = "reminders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)
    time = Column(String)
    method = Column(String)  # e.g., 'email', 'sms', etc.
    active = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="reminders")

class Partner(Base):
    __tablename__ = "partners"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    partner_user_id = Column(Integer, ForeignKey("users.id"))
    consent_type = Column(String)  # e.g., 'cycle', 'advice', etc.
    status = Column(String, default="pending")  # 'pending', 'accepted', 'revoked'

    user = relationship("User", back_populates="partners", foreign_keys=[user_id])
    partner = relationship("User", back_populates="partner_of", foreign_keys=[partner_user_id])
