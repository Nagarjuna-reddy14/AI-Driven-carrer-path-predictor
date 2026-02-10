"""
Prediction API routes.
Handles career path predictions and skill gap analysis.
"""

from fastapi import APIRouter, HTTPException, Depends
from app.api.auth import get_current_user
from app.models.schemas import UserProfileInput
from app.ml.career_predictor import predict_career_paths, analyze_skill_gaps, get_career_info
from app.core.firebase import get_firestore_client
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/career")
async def predict_careers(
    profile: UserProfileInput,
    current_user: dict = Depends(get_current_user)
):
    """
    Predict career paths based on user profile.
    
    Args:
        profile: User profile with skills and interests
        current_user: Authenticated user
        
    Returns:
        dict: Career predictions and analysis
    """
    try:
        # Combine skills from profile
        all_skills = profile.skills.copy()
        
        # Predict career paths
        predictions = predict_career_paths(all_skills, top_k=3)
        
        if not predictions:
            raise HTTPException(
                status_code=400,
                detail="Unable to generate predictions. Please add more skills."
            )
        
        # Get top career
        top_career = predictions[0]
        
        # Analyze skill gaps for top career
        skill_gaps = analyze_skill_gaps(all_skills, top_career['career_title'])
        
        # Generate analysis ID
        analysis_id = str(uuid.uuid4())
        
        # Prepare response
        result = {
            "analysis_id": analysis_id,
            "user_id": current_user['uid'],
            "predictions": predictions,
            "top_career": {
                "title": top_career['career_title'],
                "confidence": top_career['confidence'],
                "description": top_career['description'],
                "salary_range": top_career['average_salary'],
                "growth_rate": top_career['growth_rate'],
                "match_percentage": top_career['skill_match_percentage']
            },
            "skill_gaps": skill_gaps,
            "analyzed_at": datetime.utcnow().isoformat()
        }
        
        # Save to Firestore
        try:
            db = get_firestore_client()
            doc_ref = db.collection('analyses').document(analysis_id)
            doc_ref.set({
                **result,
                'user_email': current_user.get('email'),
                'created_at': datetime.utcnow()
            })
            logger.info(f"Analysis saved to Firestore: {analysis_id}")
        except Exception as e:
            logger.error(f"Failed to save to Firestore: {str(e)}")
            # Continue even if Firestore save fails
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Career prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to predict career paths")


@router.get("/careers")
async def list_careers(current_user: dict = Depends(get_current_user)):
    """
    List all available career paths.
    
    Returns:
        dict: Available careers
    """
    from app.ml.career_predictor import get_all_careers, CAREER_DATABASE
    
    careers = get_all_careers()
    
    career_list = []
    for career in careers:
        info = CAREER_DATABASE[career]
        career_list.append({
            "title": career,
            "description": info['description'],
            "category": info['category'],
            "salary_range": info['average_salary'],
            "growth_rate": info['growth_rate']
        })
    
    return {
        "careers": career_list,
        "total": len(career_list)
    }


@router.get("/career/{career_title}")
async def get_career_details(
    career_title: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get detailed information about a specific career.
    
    Args:
        career_title: Career title
        
    Returns:
        dict: Career details
    """
    try:
        info = get_career_info(career_title)
        
        return {
            "title": career_title,
            **info
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/skill-gaps/{career_title}")
async def get_skill_gaps(
    career_title: str,
    skills: list[str],
    current_user: dict = Depends(get_current_user)
):
    """
    Analyze skill gaps for a specific career.
    
    Args:
        career_title: Target career
        skills: User's current skills
        
    Returns:
        dict: Skill gap analysis
    """
    try:
        gaps = analyze_skill_gaps(skills, career_title)
        
        return {
            "career": career_title,
            **gaps
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Skill gap analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze skill gaps")
