"""
Pydantic models for request/response validation.
Defines data structures used throughout the API.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class UserProfileInput(BaseModel):
    """User profile input data."""
    education: str = Field(..., min_length=1, max_length=500)
    skills: List[str] = Field(..., min_items=1, max_items=50)
    interests: List[str] = Field(..., min_items=1, max_items=20)
    experience_years: Optional[int] = Field(0, ge=0, le=50)
    
    @validator('skills', 'interests')
    def validate_list_items(cls, v):
        """Ensure list items are non-empty strings."""
        return [item.strip() for item in v if item.strip()]


class SkillExtraction(BaseModel):
    """Extracted skills from text."""
    skills: List[str]
    categories: Dict[str, List[str]]
    confidence: float = Field(..., ge=0, le=1)


class CareerPrediction(BaseModel):
    """Career path prediction result."""
    career_title: str
    confidence: float = Field(..., ge=0, le=1)
    description: str
    average_salary: Optional[str] = None
    growth_rate: Optional[str] = None
    required_skills: List[str]
    skill_match_percentage: float = Field(..., ge=0, le=100)


class SkillGap(BaseModel):
    """Skill gap analysis."""
    missing_skills: List[str]
    partial_skills: List[str]
    matched_skills: List[str]
    gap_percentage: float = Field(..., ge=0, le=100)


class LearningResource(BaseModel):
    """Learning resource recommendation."""
    title: str
    type: str  # course, book, video, documentation
    url: Optional[str] = None
    duration: Optional[str] = None
    difficulty: str  # beginner, intermediate, advanced


class Project(BaseModel):
    """Project recommendation."""
    title: str
    description: str
    skills_practiced: List[str]
    difficulty: str
    estimated_time: str


class Certification(BaseModel):
    """Certification recommendation."""
    name: str
    provider: str
    url: Optional[str] = None
    cost: Optional[str] = None
    duration: Optional[str] = None


class LearningRoadmap(BaseModel):
    """Complete learning roadmap."""
    career_path: str
    timeline: str
    phases: List[Dict[str, Any]]
    skills_to_learn: List[str]
    tools: List[str]
    projects: List[Project]
    certifications: List[Certification]
    resources: List[LearningResource]


class AnalysisResult(BaseModel):
    """Complete analysis result."""
    user_id: str
    extracted_skills: SkillExtraction
    career_predictions: List[CareerPrediction]
    top_career: CareerPrediction
    skill_gaps: SkillGap
    roadmap: LearningRoadmap
    analyzed_at: datetime
    analysis_id: str


class TokenVerification(BaseModel):
    """Firebase token verification request."""
    token: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    """User information response."""
    uid: str
    email: str
    display_name: Optional[str] = None
    email_verified: bool
    created_at: Optional[int] = None


class ErrorResponse(BaseModel):
    """Error response model."""
    message: str
    detail: Optional[str] = None
    error_code: Optional[str] = None


class SuccessResponse(BaseModel):
    """Generic success response."""
    message: str
    data: Optional[Dict[str, Any]] = None
