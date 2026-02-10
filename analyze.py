"""
Analysis API routes.
Handles resume parsing, skill extraction, and text analysis.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Form
from app.api.auth import get_current_user
from app.ml.skill_extractor import extract_skills_from_text
from app.core.config import settings
import PyPDF2
import io
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


async def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text from PDF file.
    
    Args:
        file_content: PDF file bytes
        
    Returns:
        str: Extracted text
    """
    try:
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text.strip()
        
    except Exception as e:
        logger.error(f"PDF extraction error: {str(e)}")
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")


@router.post("/resume")
async def analyze_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Analyze resume PDF and extract skills.
    
    Args:
        file: Uploaded PDF file
        current_user: Authenticated user
        
    Returns:
        dict: Extracted skills and analysis
    """
    # Validate file type
    if file.content_type not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Only PDF files are allowed."
        )
    
    # Read file content
    try:
        content = await file.read()
        
        # Validate file size
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is {settings.MAX_UPLOAD_SIZE // 1024 // 1024}MB"
            )
        
        # Extract text from PDF
        text = await extract_text_from_pdf(content)
        
        if not text or len(text) < 50:
            raise HTTPException(
                status_code=400,
                detail="Could not extract sufficient text from PDF. Please ensure it's a text-based PDF."
            )
        
        # Extract skills
        skill_analysis = extract_skills_from_text(text)
        
        logger.info(f"Extracted {skill_analysis['total_skills_found']} skills for user {current_user['uid']}")
        
        return {
            "success": True,
            "user_id": current_user['uid'],
            "extracted_text_length": len(text),
            "skills": skill_analysis['skills'],
            "categories": skill_analysis['categories'],
            "confidence": skill_analysis['confidence'],
            "total_skills_found": skill_analysis['total_skills_found']
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Resume analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze resume")


@router.post("/text")
async def analyze_text(
    text: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Analyze text and extract skills.
    
    Args:
        text: Input text to analyze
        current_user: Authenticated user
        
    Returns:
        dict: Extracted skills and analysis
    """
    if not text or len(text) < 20:
        raise HTTPException(
            status_code=400,
            detail="Text too short. Please provide at least 20 characters."
        )
    
    try:
        # Extract skills
        skill_analysis = extract_skills_from_text(text)
        
        logger.info(f"Extracted {skill_analysis['total_skills_found']} skills from text for user {current_user['uid']}")
        
        return {
            "success": True,
            "user_id": current_user['uid'],
            "skills": skill_analysis['skills'],
            "categories": skill_analysis['categories'],
            "confidence": skill_analysis['confidence'],
            "total_skills_found": skill_analysis['total_skills_found']
        }
        
    except Exception as e:
        logger.error(f"Text analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze text")


@router.get("/skills/categories")
async def get_skill_categories(current_user: dict = Depends(get_current_user)):
    """
    Get available skill categories.
    
    Returns:
        dict: Skill categories
    """
    from app.ml.skill_extractor import SKILL_DATABASE
    
    categories = {
        category: len(skills) 
        for category, skills in SKILL_DATABASE.items()
    }
    
    return {
        "categories": categories,
        "total_categories": len(categories)
    }
